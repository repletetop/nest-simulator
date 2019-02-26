# -*- coding: utf-8 -*-
#
# test_errors.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

"""
Tests for error handling
"""

import unittest
import nest


@nest.ll_api.check_stack
class ErrorTestCase(unittest.TestCase):
    """Tests if errors are handled correctly"""

    def test_Raise(self):
        """Error raising"""

        def raise_custom_exception(exc, msg):
            raise exc(msg)

        message = "test"
        exception = nest.kernel.NESTError

        self.assertRaisesRegex(
            exception, message, raise_custom_exception, exception, message)

    def test_StackUnderFlow(self):
        """Stack underflow"""

        nest.ResetKernel()

        self.assertRaisesRegex(
            nest.kernel.NESTError, "StackUnderflow", nest.ll_api.sr, 'clear ;')

    def test_DivisionByZero(self):
        """Division by zero"""

        nest.ResetKernel()

        self.assertRaisesRegex(
            nest.kernel.NESTError, "DivisionByZero", nest.ll_api.sr, '1 0 div')

    def test_InvalidGIDCollection(self):
        """Invalid GIDCollection"""

        nest.ResetKernel()

        gc1 = nest.Create('iaf_psc_alpha', 10)
        gc2 = nest.Create('iaf_psc_alpha', 10)
        gc3 = nest.Create('iaf_psc_exp', 10)
        gc_c = gc1 + gc3

        nest.ResetKernel()

        def add_test_primitive():
            return gc1 + gc2

        def add_test_composite():
            return gc1 + gc3

        def add_test_pc():
            return gc_c + gc2

        def slice_test_primitive():
            return gc1[8:9]

        def slice_test_composite():
            return gc_c[8:9]

        self.assertRaisesRegexp(
            nest.kernel.NESTError, "InvalidGIDCollection", add_test_primitive)

        self.assertRaisesRegexp(
            nest.kernel.NESTError, "InvalidGIDCollection", add_test_composite)

        self.assertRaisesRegexp(
            nest.kernel.NESTError, "InvalidGIDCollection", add_test_pc)

        self.assertRaisesRegexp(
            nest.kernel.NESTError, "InvalidGIDCollection", slice_test_primitive)

        self.assertRaisesRegexp(
            nest.kernel.NESTError, "InvalidGIDCollection", slice_test_composite)

    def test_UnknownNode(self):
        """Unknown node"""

        nest.ResetKernel()

        gc = nest.Create('iaf_psc_alpha', 10)
        nest.ResetKernel()

        self.assertRaisesRegexp(
            nest.kernel.NESTError, "UnknownNode", nest.GIDCollection, [99])

    def test_UnknownModel(self):
        """Unknown model name"""

        nest.ResetKernel()

        self.assertRaisesRegex(
            nest.kernel.NESTError, "UnknownModelName", nest.Create, -1)


def suite():
    suite = unittest.makeSuite(ErrorTestCase, 'test')
    return suite


def run():
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

if __name__ == "__main__":
    run()
