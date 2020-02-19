#!/usr/bin/python
# # coding=utf-8

import os
import shutil
import pytest
import tensorflow as tf


def test_load_format_data_train_ds(get_data):
    assert type(get_data.train_ds) == tf.python.data.ops.dataset_ops.DatasetV1Adapter


def test_load_format_data_test_ds(get_data):
    assert type(get_data.test_ds) == tf.python.data.ops.dataset_ops.DatasetV1Adapter


def test_define_model(get_model):
    assert get_model.model is not None


def test_train_model(train):
    assert train.history is not None


def test_evaluate_performance(evaluate):
    assert evaluate.train_accuracy is not None


def test_persistence_criteria(evaluate):
    """Check that the system exits when target criteria is not met by the trained model.

    :param evaluate: pytest fixture, defined in conftest.py
    :type evaluate: pytest.fixture
    """
    evaluate.target_accuracy = 1.00
    with pytest.raises(SystemExit):
        evaluate.persistence_criteria()


def test_convert_save_onnx(evaluate):
    if os.path.exists('model.onnx'):
        os.remove('model.onnx')
    evaluate.convert_save_onnx()
    assert os.path.exists('model.onnx')


def test_save_metrics(evaluate):
    if os.path.exists('./metrics'):
        shutil.rmtree('./metrics')
    evaluate.save_metrics()
    assert os.path.exists('./metrics/testloss.metric')
    shutil.rmtree('./metrics')
