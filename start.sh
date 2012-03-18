#!/bin/bash

PYTHONPATH=api/ twistd --pidfile=log/api.pid --logfile=log/api.log -noy api/app.tac
