# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import mock

sys.path.append('lib')

# Mock out charmhelpers so that we can test without it.
# also stops sideeffects from occuring.
apt_pkg = mock.MagicMock()
charmhelpers = mock.MagicMock()
sys.modules['apt_pkg'] = apt_pkg
sys.modules['charmhelpers'] = charmhelpers
sys.modules['charmhelpers.core'] = charmhelpers.core
sys.modules['charmhelpers.core.hookenv'] = charmhelpers.core.hookenv
sys.modules['charmhelpers.fetch'] = charmhelpers.fetch
sys.modules['charmhelpers.cli'] = charmhelpers.cli
