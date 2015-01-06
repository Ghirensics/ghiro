# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file "docs/LICENSE.txt" for license terms.

from lib.analyzer.base import BaseAnalyzerModule, BaseSignature
from copy import deepcopy

try:
    import plugins.signatures.default
    HAS_SIGNS = True
except ImportError:
    HAS_SIGNS = False


class SignatureAnalyzer(BaseAnalyzerModule):
    """Run signatures on results data."""

    order = 80

    def check_deps(self):
        return HAS_SIGNS

    def run(self, task):
        matches = []
        for sign in BaseSignature.__subclasses__():
            try:
                sign = sign()
                # Casting results to dict to avoid auto key creation.
                # NOTE: deepcopy is used to run signatures on a copy to avoid creation
                # of empty Autovivification dict keys.
                match = sign.check(deepcopy(self.data))
            except KeyError:
                continue
            except Exception as e:
                print e
                continue

            if match:
                foo = {
                       "id": sign.pk,
                       "name": sign.name,
                       "category": sign.category,
                       "severity": sign.severity,
                       "description": sign.description
                       }
                if isinstance(match, tuple):
                    foo["data"] = match
                matches.append(foo)

        self.results["signatures"] = matches

        return self.results
