# ----------------------------------------------------------------------------
# Copyright 2017 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

from __future__ import print_function, division
import numpy as np

from ngraph.frontends.onnx.tests.test_ops_unary import import_and_compute


def assert_onnx_import_equals_callable(onnx_op_type, python_function, data, **kwargs):
    data = np.array(data, dtype=np.float32)
    assert np.allclose(import_and_compute(onnx_op_type, data, **kwargs),
                       python_function(data, **kwargs))


def test_sigmoid():
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    assert_onnx_import_equals_callable('Sigmoid', sigmoid, [-2, -1., 0., 1., 2.])
    assert_onnx_import_equals_callable('Sigmoid', sigmoid, [0.])
    assert_onnx_import_equals_callable('Sigmoid', sigmoid, [-2, -1., 0., 1., 2.])


def test_tanh():
    assert_onnx_import_equals_callable('Tanh', np.tanh, [-2, -1., 0., 1., 2.])
    assert_onnx_import_equals_callable('Tanh', np.tanh, [0.])
    assert_onnx_import_equals_callable('Tanh', np.tanh, [-2, -1., 0., 1., 2.])


def test_relu():
    def relu(x):
        return np.maximum(x, 0)

    assert_onnx_import_equals_callable('Relu', relu, [-2, -1., 0., 1., 2.])
    assert_onnx_import_equals_callable('Relu', relu, [0.])
    assert_onnx_import_equals_callable('Relu', relu, [-0.9, -0.8, -0.7, -0.4, -0.3, -0.2, -0.1])
    assert_onnx_import_equals_callable('Relu', relu, [[1, 2, 3], [4, 5, 6]])
    assert_onnx_import_equals_callable('Relu', relu, [[-3, -2, -1], [1, 2, 3]])


def test_leaky_relu():
    def leaky_relu(x, alpha=0.01):
        return np.maximum(alpha * x, 0)

    assert_onnx_import_equals_callable('LeakyRelu', leaky_relu,
                                       [-2, -1., 0., 1., 2.], alpha=0.5)
    assert_onnx_import_equals_callable('LeakyRelu', leaky_relu, [0.])
    assert_onnx_import_equals_callable('LeakyRelu', leaky_relu,
                                       [-0.9, -0.8, -0.7, -0.4, -0.3, -0.2, -0.1], alpha=1)
    assert_onnx_import_equals_callable('LeakyRelu', leaky_relu,
                                       [[1, 2, 3], [4, 5, 6]], alpha=0.2)
    assert_onnx_import_equals_callable('LeakyRelu', leaky_relu,
                                       [[-3, -2, -1], [1, 2, 3]])


def test_parametric_relu():
    def parametic_relu(x, slope=0.01):
        return np.where(x < 0, slope * x, x)

    assert_onnx_import_equals_callable('PRelu', parametic_relu,
                                       [-2, -1., 0., 1., 2.], slope=0.5)
    assert_onnx_import_equals_callable('PRelu', parametic_relu, [0.])
    assert_onnx_import_equals_callable('PRelu', parametic_relu,
                                       [-0.9, -0.8, -0.7, -0.4, -0.3, -0.2, -0.1], slope=1)
    assert_onnx_import_equals_callable('PRelu', parametic_relu,
                                       [[1, 2, 3], [4, 5, 6]], slope=0.2)
    assert_onnx_import_equals_callable('PRelu', parametic_relu,
                                       [[-3, -2, -1], [1, 2, 3]])


def test_selu():
    # f(x) = gamma * (alpha * exp(x) - alpha) for x <= 0, y = gamma * x for x > 0
    def selu(x, alpha=1.6732, gamma=1.0507):
        return np.where(x <= 0, gamma * (alpha * np.exp(x) - alpha), gamma * x)

    assert_onnx_import_equals_callable('Selu', selu,
                                       [-2, -1., 0., 1., 2.])
    assert_onnx_import_equals_callable('Selu', selu, [0.])
    assert_onnx_import_equals_callable('Selu', selu,
                                       [-0.9, -0.8, -0.7, -0.4, -0.3, -0.2, -0.1])
    assert_onnx_import_equals_callable('Selu', selu,
                                       [[1, 2, 3], [4, 5, 6]])
    assert_onnx_import_equals_callable('Selu', selu,
                                       [-2, -1., 0., 1., 2.], gamma=0.5, alpha=0.5)


def test_elu():
    # f(x) = alpha * (exp(x) - 1) for x < 0, f(x) = x for x >= 0
    def elu(x, alpha=1):
        return np.where(x < 0, alpha * (np.exp(x) - 1), x)

    assert_onnx_import_equals_callable('Elu', elu,
                                       [-2, -1., 0., 1., 2.])
    assert_onnx_import_equals_callable('Elu', elu, [0.])
    assert_onnx_import_equals_callable('Elu', elu,
                                       [-0.9, -0.8, -0.7, -0.4, -0.3, -0.2, -0.1])
    assert_onnx_import_equals_callable('Elu', elu,
                                       [[1, 2, 3], [4, 5, 6]])
    assert_onnx_import_equals_callable('Elu', elu,
                                       [-2, -1., 0., 1., 2.], alpha=0.5)
