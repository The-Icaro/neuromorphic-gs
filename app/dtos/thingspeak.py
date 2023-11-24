from typing import List
from dataclasses import dataclass, field
from datetime import date

from dataclasses_json import dataclass_json, Undefined, config


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=False)
class FeedBase:
    pulse_rate: float = field(metadata=config(field_name="field1"), default=0.0)
    temperature: float = field(metadata=config(field_name="field2"), default=0.0)
    air_quality: float = field(metadata=config(field_name="field3"), default=0.0)
    created_at: date = field(metadata=config(field_name="created_at"), default=0.0)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=False)
class ThingspeakResponse:
    feeds: List[FeedBase] = field(default=None)
