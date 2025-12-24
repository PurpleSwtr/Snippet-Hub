#!/bin/bash

cd Backend
uv run uvicorn src.main:app --reload