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
                             'height' : 350,
                             'width' : 320,
                             'tab' : 1,
                             'icon' : 'wait4digits.png',
                             'maxconn' : { 'source' : -1, 'target' : -1 },
                             'input' :  { 'wait_prompt_path' : 'Prompt File Path (optional)',
                                          'timeout' : 'Timeout (in seconds)'
                                       },
                           }


        self.prompts = { 'title' : 'Prompts properties ...',
                         'height' : 350,
                         'width' : 320,
                         'tab' : 1,
                         'icon' : 'prompts.png',
                         'input' : { 'prompt_path' : 'Prompt File Path' },
                       }

        self.execute = { 'title' : 'Execute properties ...',
                         'height' : 350,
                         'width' : 320,
                         'tab' : 1,
                         'icon' : 'execute.png',
                         'input' : { 'application' : 'Asterisk application', 'arguments' : 'Arguments' },
                       }

        self.start = { 'title' : 'Start properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'start.png',
                       'input' : { 'extension' : 'Extension (optionnal)' },
                     }

        self.voicemail = { 'title' : 'Voicemail properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'voicemail.png',
                       'input' : { 'mailbox' : 'Mailbox number' },
                     }

        self.debug = { 'title' : 'Debug properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 1,
                       'icon' : 'debug.png',
                       'input' : { 'arguments' : 'Arguments' },
                     }

        self.language = { 'title' : 'Language properties ...',
                          'height' : 350,
                          'width' : 320,
                          'tab' : 1,
                          'icon' : 'language.png',
                          'input' : { 'language' : 'Language' },
                        }

        self.authenticate = { 'title' : 'Language properties ...',
                              'height' : 300,
                              'width' : 320,
                              'tab' : 2,
                              'icon' : 'authenticate.png',
                              'input' : { 'code' : 'Code', 'maxdigits' : 'Maximum digits (user need to finish with #)' },
                            }

        self.switchivr = { 'title' : 'Goto to another IVR properties ...',
                           'height' : 300,
                           'width' : 320,
                           'tab' : 2,
                           'maxconn' : { 'source' : 0, 'target' : -1 },
                           'icon' : 'authenticate.png',
                           'input' : { 'context' : 'Context name (without auto prefix)', 'start' : 'Number of the start IVR (s if you haven\'t one' },
                         }

        self.directory = { 'title' : 'Directory properties ...',
                           'height' : 350,
                           'width' : 320,
                           'tab' : 2,
                           'icon' : 'directory.png',
                           'input' : { 'vmcontext' : 'Voicemail context name' },
                        }

        self.read = { 'title' : 'Read properties ...',
                      'height' : 350,
                      'width' : 320,
                      'tab' : 2,
                      'icon' : 'read.png',
                      'input' : { 'variable' : 'Variable', 'timeout' : 'Timeout', 'prompt' : 'Prompt', 'maxdigits' : 'Max digits' },
                    }

        self.dial = { 'title' : 'Dial properties ...',
                      'height' : 350,
                      'width' : 320,
                      'tab' : 1,
                      'icon' : 'dial.png',
                      'input' : { 'arguments' : 'Arguments' },
                    }

        self.answer = { 'title' : 'Answer properties ...',
                        'height' : 350,
                        'width' : 320,
                        'tab' : 1,
                        'icon' : 'answer.png',
                        'input' : { 'timeout' : 'Timeout' },
                      }

        self.gotoif = { 'title' : 'Gotoif properties ...',
                        'height' : 350,
                        'width' : 320,
                        'tab' : 2,
                        'maxconn' : { 'source' : 2, 'target' : 1 },
                        'icon' : 'gotoif.png',
                        'input' : { 'expression' : 'Expression' },
                      }

        self.gotoiftime = { 'title' : 'Gotoiftime properties ...',
                            'height' : 350,
                            'width' : 320,
                            'tab' : 2,
                            'maxconn' : { 'source' : 2, 'target' : 1 },
                            'icon' : 'gotoiftime.png',
                            'input' : { 'expression' : 'Expression (ex. *,*,24,jun)' },
                          }

        self.setvar = { 'title' : 'Set variable properties ...',
                        'height' : 350,
                        'width' : 320,
                        'tab' : 2,
                        'icon' : 'setvar.png',
                        'input' : { 'variable' : 'Variable Name', 'value' : 'Values' },
                      }

        self.goto = { 'title' : 'Goto properties ...',
                      'height' : 350,
                      'width' : 320,
                      'tab' : 2,
                      'icon' : 'goto.png',
                      'input' : { 'arguments' : 'Arguments' },
                      }

        self.wait = { 'title' : 'Wait properties ...',
                      'height' : 350,
                      'width' : 320,
                      'tab' : 2,
                      'icon' : 'wait.png',
                      'input' : { 'timeout' : 'Timeout' },
                      }

        self.busy = { 'title' : 'Busy properties ...',
                      'height' : 350,
                      'width' : 320,
                      'tab' : 2,
                      'icon' : 'busy.png',
                      'input' : { 'timeout' : 'Timeout' },
                      }

        self.congestion = { 'title' : 'Congestion properties ...',
                            'height' : 350,
                            'width' : 320,
                            'tab' : 2,
                            'icon' : 'congestion.png',
                            'input' : { 'timeout' : 'Timeout' },
                          }

        self.monitor = { 'title' : 'Monitor properties ...',
                         'height' : 350,
                         'width' : 320,
                         'tab' : 2,
                         'icon' : 'monitor.png',
                         'input' : { 'filename' : 'Filename (optional)' },
                       }

        self.saydigits = { 'title' : 'Saydigits properties ...',
                           'height' : 350,
                           'width' : 320,
                           'tab' : 2,
                           'icon' : 'saydigits.png',
                           'input' : { 'digits' : 'Digits' },
                         }

        self.wait4ring = { 'title' : 'Wait for ring properties ...',
                           'height' : 350,
                           'width' : 320,
                           'tab' : 2,
                           'icon' : 'wait4ring.png',
                           'input' : { 'timeout' : 'Timeout' },
                         }

        self.wait4silence = { 'title' : 'Wait for silence properties ...',
                              'height' : 350,
                              'width' : 320,
                              'tab' : 2,
                              'icon' : 'wait4silence.png',
                              'input' : { 'timeout' : 'Timeout' },
                           }

        self.wait4music = { 'title' : 'Wait for silence properties ...',
                            'height' : 350,
                            'width' : 320,
                            'tab' : 2,
                            'icon' : 'wait4silence.png',
                            'input' : { 'timeout' : 'Timeout', 'musicclass' : 'Music class' },
                         }

        self.dbexists = { 'title' : 'DBExists properties ...',
                          'height' : 350,
                          'width' : 320,
                          'tab' : 2,
                          'maxconn' : { 'source' : 2, 'target' : 1 },
                          'icon' : 'dbexists.png',
                          'input' : { 'key' : 'Family/key' },
                         }

        self.dbput = { 'title' : 'DBPut properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 2,
                       'icon' : 'dbput.png',
                       'input' : { 'key' : 'Family/key', 'value' : 'Value' },
                     }

        self.dbget = { 'title' : 'DBGet properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 2,
                       'icon' : 'dbget.png',
                       'input' : { 'key' : 'Family/key', 'variable' : 'Variable' },
                     }

        self.dbdel = { 'title' : 'DBDelete properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 2,
                       'icon' : 'dbdel.png',
                       'input' : { 'key' : 'Family/key' },
                     }

        self.dbdeltree = { 'title' : 'DBDeltree properties ...',
                           'height' : 350,
                           'width' : 320,
                           'tab' : 2,
                           'icon' : 'dbdeltree.png',
                           'input' : { 'key' : 'Family/key' },
                          }

        self.gosub = { 'title' : 'Gosub properties ...',
                       'height' : 350,
                       'width' : 320,
                       'tab' : 2,
                       'icon' : 'gosub.png',
                       'input' : { 'arguments' : 'Arguments' },
                     }

        self.celgenuser = { 'title' : 'CELGenUserEvent properties ...',
                            'height' : 350,
                            'width' : 320,
                            'tab' : 2,
                            'icon' : 'celgenuser.png',
                            'input' : { 'event' : 'Event name', 'extra' : 'Extra info' },
                           }

        self.agi = { 'title' : 'AGI properties ...',
                     'height' : 350,
                     'width' : 320,
                     'tab' : 2,
                     'icon' : 'agi.png',
                     'input' : { 'command' : 'Command', 'arguments' : 'Arguments' },
                   }
 
        self.callerid = { 'title' : 'CallerID properties ...',
                          'height' : 350,
                          'width' : 320,
                          'tab' : 2,
                          'icon' : 'callerid.png',
                          'input' : { 'name' : 'Name' },
                        }

        self.voicemailmain = { 'title' : 'CallerID properties ...',
                               'height' : 350,
                               'width' : 320,
                               'tab' : 2,
                               'icon' : 'voicemailmain.png',
                               'input' : { 'mailbox' : 'Mailbox', 'options' : 'Options' },
                             }

    def getJsonactions(self):
        for act in self.__dict__.items():
            if act[0] != 'actions':
                self.actions.update({act[0] : act[1]})

        return json.dumps(self.actions)

