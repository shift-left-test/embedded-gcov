# -*- coding: utf-8 -*-

"""
Copyright (c) 2023 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import shutil
import subprocess
import pytest


@pytest.fixture(scope="session")
def binary_to_gcda(request, tmpdir_factory):
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)

    project_dir = os.path.join(os.path.dirname(__file__), "..")

    subprocess.check_call(
        f'cd {build_dir} && gcc -Wall -O0 -fprofile-arcs -ftest-coverage -o example {project_dir}/example/example.c {project_dir}/code/gcov_public.c {project_dir}/code/gcov_gcc.c {project_dir}/code/gcov_printf.c -D GCOV_OPT_OUTPUT_BINARY_FILE && ./example',
        shell=True)
    stdout = subprocess.check_output(
        f"cd {build_dir} && {project_dir}/scripts/binary_to_gcda.py gcov_output.bin && gcov example && gcov gcov_public",
        stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    return stdout


def test_binary_to_gcda_output(binary_to_gcda):
    assert "gcov_printf.gcda" in binary_to_gcda
    assert "gcov_gcc.gcda" in binary_to_gcda
    assert "gcov_public.gcda" in binary_to_gcda
    assert "example.gcda" in binary_to_gcda


def test_make_gcov_from_gcda(binary_to_gcda):
    assert "Lines executed:85.71% of 7" in binary_to_gcda
    assert "Lines executed:80.65% of 93" in binary_to_gcda
