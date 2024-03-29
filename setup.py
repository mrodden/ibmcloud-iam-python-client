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

with open("README.md", "r", encoding="utf8") as fh:
    long_desc = fh.read()

setup(
    name="ibmcloud-iam",
    version="0.1.7",
    author="Mathew Odden",
    author_email="mrodden@us.ibm.com",
    url="https://github.com/mrodden/ibmcloud-iam-python-client",
    description="A collection of Python modules used for interacting with IBMCloud IAM API services",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"ibmcloud_iam": ["py.typed", "*.pyi"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests[security]", "pyjwt>=2.1.0,<2.5", "redstone"],
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
    python_requires=">=3.6",
)
