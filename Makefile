.PHONY: all

-include .env

SHELL=/bin/bash -e

.DEFAULT_GOAL := help

help:
		@echo "make run"
		@echo "		Run server"
		@echo "make migrate"
		@echo "		Run db migration"

run:
		uvicorn app.main:app --reload

migrate:
		aerich upgrade
