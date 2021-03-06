# syntax=docker/dockerfile:experimental
#
# Copyright 2018-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Ubuntu 18.04 LTS - Bionic
FROM jupyterhub/k8s-singleuser-sample:0.10.6

ARG TAG="dev"

USER root

ADD start-elyra.sh /usr/local/bin/start-elyra.sh

RUN chmod ugo+x /usr/local/bin/start-elyra.sh && \
    if [ "$TAG" == "dev" ] ; then \
       apt-get update && apt-get install -y build-essential && \
       rm -rf /var/lib/apt/lists/*; \
    fi

USER $NB_USER

RUN conda remove --force -y terminado && \
    python -m pip install --upgrade pip && \
    python -m pip install --ignore-installed --upgrade setuptools pandas && \
    npm config set scripts-prepend-node-path auto && \
    npm config get prefix /home/jovyan/.npm-global && \
    mkdir -p /home/jovyan/.npm-global && \
    if [ "$TAG" == "dev" ] ; then \
       npm install -g yarn && \
       npm install -g npm && \
       cd /tmp && git clone https://github.com/elyra-ai/elyra.git && \
       cd /tmp/elyra && make UPGRADE_STRATEGY=eager install && rm -rf /tmp/elyra; \
    else \
        python3 -m pip install --quiet --no-cache-dir --use-deprecated=legacy-resolver elyra=="$TAG" && \
        jupyter lab build; \
    fi

CMD ["/usr/local/bin/start-elyra.sh"]

