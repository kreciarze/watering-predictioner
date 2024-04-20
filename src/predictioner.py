import pickle  # noqa: S403

from config import MODEL_PICKLE_FILENAME
from record import Record

with open(f"src/{MODEL_PICKLE_FILENAME}", "rb") as f:
    classifier = pickle.load(f)  # noqa: S301


def decide_whether_to_water(record: Record) -> bool:
    result = classifier.predict(record.to_df())
    return bool(result[0])
