# Copyright 2021 Mathew Odden
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

from setuptools import setup, find_packages

setup(
    name="ibmcloud-iam",
    version="0.1.0",
    author="Mathew Odden",
    author_email="mrodden@us.ibm.com",
    url="https://github.com/mrodden/ibmcloud-iam-python-client",
    packages=find_packages(),
    install_requires=["requests[security]", "pyjwt", "redstone"],
    extras_require={
        "docs": ["sphinx>=3.1", "sphinx_rtd_theme"],
    },
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ],
)
