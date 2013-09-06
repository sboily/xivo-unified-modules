# -*- coding: utf-8 -*-

# Copyright (C) 2013 Sylvain Boily <sboily@proformatique.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

class ivrActions(object):

    def __init__(self):
        self.actions = {}

        self.wait4digits = { 'title' : 'Wait4digits properties ...',
                             'height' : 400,
                             'width' : 600,
                             'tab' : 1,
                             'icon' : 'wait4digits.png',
                             'maxconn' : { 'source' : -1, 'target' : -1 },
                             'input' :  { 'wait_prompt_path' : 'Prompt File Path (optional)',
                                          'min_digits' : 'Min no of digits expected',
                                          'max_digits' : 'Max no of digits expected',
                                          'wait_expected_digits' : 'Expected Digits',
                                          'retries' : 'Retries',
                                          'retry_timeout' : 'Retry timeout (in seconds)'
                                       },
                             'textarea' : { 'description' : 'Description' }
                           }


        self.prompts = { 'title' : 'Prompts properties ...',
                         'height' : 270,
                         'width' : 500,
                         'tab' : 1,
                         'icon' : 'prompts.png',
                         'input' : { 'prompt_path' : 'Prompt File Path' },
                         'textarea' : { 'description' : 'Description' }
                       }

        self.execute = { 'title' : 'Execute properties ...',
                         'height' : 270,
                         'width' : 500,
                         'tab' : 1,
                         'icon' : 'execute.png',
                         'input' : { 'application' : 'Asterisk application', 'arguments' : 'Arguments' },
                         'textarea' : { 'description' : 'Description' }
                       }

        self.start = { 'title' : 'Start properties ...',
                       'height' : 300,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'start.png',
                       'input' : { 'extension' : 'Extension (optionnal)' },
                       'textarea' : { 'description' : 'Description' }
                     }

        self.voicemail = { 'title' : 'Voicemail properties ...',
                       'height' : 300,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'voicemail.png',
                       'input' : { 'mailbox' : 'Mailbox number' },
                       'textarea' : { 'description' : 'Description' }
                     }

        self.debug = { 'title' : 'Debug properties ...',
                       'height' : 300,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'debug.png',
                       'input' : { 'arguments' : 'Arguments' },
                       'textarea' : { 'description' : 'Description' }
                     }

        self.func = { 'title' : 'Function properties ...',
                       'height' : 300,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'func.png',
                       'input' : { 'name' : 'Name' },
                       'textarea' : { 'function' : 'Function', 'description' : 'Description' }
                     }

        self.language = { 'title' : 'Language properties ...',
                          'height' : 300,
                          'width' : 320,
                          'tab' : 1,
                          'icon' : 'language.png',
                          'input' : { 'language' : 'Language' },
                          'textarea' : { 'description' : 'Description' }
                        }

        self.authenticate = { 'title' : 'Language properties ...',
                              'height' : 300,
                              'width' : 320,
                              'tab' : 2,
                              'icon' : 'authenticate.png',
                              'input' : { 'code' : 'Code', 'maxdigits' : 'Maximum digits (user need to finish with #)' },
                              'textarea' : { 'description' : 'Description' }
                        }

        self.switchivr = { 'title' : 'Goto to another IVR properties ...',
                              'height' : 300,
                              'width' : 320,
                              'tab' : 2,
                              'icon' : 'authenticate.png',
                              'input' : { 'context' : 'Context name (without auto prefix)', 'start' : 'Number of the start IVR (s if you haven\'t one' },
                              'textarea' : { 'description' : 'Description' }
                        }

        self.directory = { 'title' : 'Directory properties ...',
                           'height' : 300,
                           'width' : 320,
                           'tab' : 2,
                           'icon' : 'directory.png',
                           'input' : { 'vmcontext' : 'Voicemail context name' },
                           'textarea' : { 'description' : 'Description' }
                        }

    def getJsonactions(self):
        for act in self.__dict__.items():
            if act[0] != 'actions':
                self.actions.update({act[0] : act[1]})

        return json.dumps(self.actions)

