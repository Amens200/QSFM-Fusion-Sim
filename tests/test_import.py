def test_import():
    import qsfm_fusion.fusion_simulation as fs
    assert hasattr(fs, '__file__')
