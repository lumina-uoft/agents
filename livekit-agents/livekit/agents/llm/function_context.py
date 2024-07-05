# Copyright 2023 LiveKit, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import asyncio
import enum
import functools
import inspect
import typing
from dataclasses import dataclass
from typing import Any, Callable

METADATA_ATTR = "__livekit_ai_metadata__"
USE_DOCSTRING = _UseDocMarker()


@dataclass(frozen=True)
class TypeInfo:
    description: str = ""
    choices: list[Any] = field(default_factory=list)


@dataclass(frozen=True)
class FunctionArgInfo:
    name: str
    description: str
    type: type
    default: Any
    choices: list[Any] | None


@dataclass(frozen=True)
class FunctionInfo:
    name: str
    description: str
    auto_retry: bool
    callable: Callable
    arguments: dict[str, FunctionArgInfo]


@dataclass
class FunctionCallInfo:
    tool_call_id: str
    function_info: FunctionInfo
    raw_arguments: str
    arguments: dict[str, Any]

    def execute(self) -> CalledFunction:
        function_info = self.function_info
        func = functools.partial(function_info.callable, **self.arguments)
        if asyncio.iscoroutinefunction(function_info.callable):
            task = asyncio.create_task(func())
        else:
            task = asyncio.create_task(asyncio.to_thread(func))

        called_fnc = CalledFunction(call_info=self, task=task)

        def _on_done(fut):
            try:
                called_fnc.result = fut.result()
            except BaseException as e:
                called_fnc.exception = e

        task.add_done_callback(_on_done)
        return called_fnc


@dataclass
class CalledFunction:
    call_info: FunctionCallInfo
    task: asyncio.Task[Any]
    result: Any | None = None
    exception: BaseException | None = None


def ai_callable(
    *,
    name: str | None = None,
    desc: str | None = None,
    auto_retry: bool = True,
) -> Callable:
    def deco(f):
        metadata = AIFncMetadata(
            name=name or f.__name__,
            desc=desc or "",
            auto_retry=auto_retry,
        )

        setattr(f, METADATA_ATTR, metadata)
        return f

    return deco


@dataclass(frozen=True)
class TypeInfo:
    desc: str = ""


class FunctionContext(abc.ABC):
    def __init__(self) -> None:
        self._fncs = dict[str, AIFunction]()

        # retrieve ai functions & metadata
        for _, member in inspect.getmembers(self, predicate=inspect.ismethod):
            if not hasattr(member, METADATA_ATTR):
                continue

            metadata: AIFncMetadata = getattr(member, METADATA_ATTR)
            if metadata.name in self._fncs:
                raise ValueError(f"Duplicate function name: {metadata.name}")

            sig = inspect.signature(member)
            type_hints = typing.get_type_hints(member)  # Annotated[T, ...] -> T
            args = dict()

            for name, param in sig.parameters.items():
                if param.kind not in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                ):
                    raise ValueError(
                        f"unsupported parameter kind inside ai_callable: {param.kind}"
                    )

                if param.annotation is inspect.Parameter.empty:
                    raise ValueError(f"missing type annotation for parameter {name}")

                th = type_hints[name]

                if not is_type_supported(th):
                    raise ValueError(f"unsupported type {th} for parameter {name}")

                default = param.default

                type_info = _find_param_type_info(param.annotation)
                desc = type_info.desc if type_info else ""

                args[name] = AIFncArg(
                    name=name,
                    desc=desc,
                    type=th,
                    default=default,
                )

            aifnc = AIFunction(metadata=metadata, fnc=member, args=args)
            self._fncs[metadata.name] = aifnc

    @property
    def ai_functions(self) -> dict[str, AIFunction]:
        return self._fncs


def _find_param_type_info(annotation: type) -> TypeInfo | None:
    if typing.get_origin(annotation) is not typing.Annotated:
        return None

    for a in typing.get_args(annotation):
        if isinstance(a, TypeInfo):
            return a

    return None


# internal metadata
@dataclass(frozen=True)
class AIFncMetadata:
    name: str = ""
    desc: str = ""
    auto_retry: bool = True


@dataclass(frozen=True)
class AIFncArg:
    name: str
    desc: str
    type: type
    default: Any


@dataclass(frozen=True)
class AIFunction:
    metadata: AIFncMetadata
    fnc: Callable
    args: dict[str, AIFncArg]


def is_type_supported(t: type) -> bool:
    if t in (str, int, float, bool):
        return True

    if issubclass(t, enum.Enum):
        initial_type = None
        for e in t:
            if initial_type is None:
                initial_type = type(e.value)
            if type(e.value) is not initial_type:
                return False

        return initial_type in (str, int)

    return False
