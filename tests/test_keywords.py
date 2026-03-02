"""Tests for GAMESS keywords database."""

import pytest
from gamess_lsp.keywords import GAMESS_KEYWORDS, GAMESS_GROUPS


class TestGAMESSGroups:
    """Test GAMESS_GROUPS dictionary."""

    def test_groups_is_dict(self):
        """Test that GAMESS_GROUPS is a dictionary."""
        assert isinstance(GAMESS_GROUPS, dict)

    def test_groups_not_empty(self):
        """Test that GAMESS_GROUPS is not empty."""
        assert len(GAMESS_GROUPS) > 0

    def test_groups_contain_contrl(self):
        """Test that CONTRL group is present."""
        assert "CONTRL" in GAMESS_GROUPS
        assert isinstance(GAMESS_GROUPS["CONTRL"], str)

    def test_groups_contain_basis(self):
        """Test that BASIS group is present."""
        assert "BASIS" in GAMESS_GROUPS

    def test_groups_contain_scf(self):
        """Test that SCF group is present."""
        assert "SCF" in GAMESS_GROUPS

    def test_all_values_are_strings(self):
        """Test that all group descriptions are strings."""
        for group_name, description in GAMESS_GROUPS.items():
            assert isinstance(group_name, str)
            assert isinstance(description, str)
            assert len(description) > 0


class TestGAMESSKeywords:
    """Test GAMESS_KEYWORDS dictionary."""

    def test_keywords_is_dict(self):
        """Test that GAMESS_KEYWORDS is a dictionary."""
        assert isinstance(GAMESS_KEYWORDS, dict)

    def test_keywords_not_empty(self):
        """Test that GAMESS_KEYWORDS is not empty."""
        assert len(GAMESS_KEYWORDS) > 0

    def test_contrl_keywords(self):
        """Test that CONTRL keywords exist."""
        assert "CONTRL" in GAMESS_KEYWORDS
        contrl = GAMESS_KEYWORDS["CONTRL"]
        assert isinstance(contrl, dict)
        assert "RUNTYP" in contrl
        assert "SCFTYP" in contrl

    def test_basis_keywords(self):
        """Test that BASIS keywords exist."""
        assert "BASIS" in GAMESS_KEYWORDS
        basis = GAMESS_KEYWORDS["BASIS"]
        assert isinstance(basis, dict)
        assert "GBASIS" in basis

    def test_scf_keywords(self):
        """Test that SCF keywords exist."""
        assert "SCF" in GAMESS_KEYWORDS
        scf = GAMESS_KEYWORDS["SCF"]
        assert isinstance(scf, dict)
        assert "DIRSCF" in scf

    def test_keyword_structure(self):
        """Test keyword structure has doc and values."""
        for group, keywords in GAMESS_KEYWORDS.items():
            assert isinstance(group, str)
            assert isinstance(keywords, dict)
            for keyword_name, keyword_info in keywords.items():
                assert isinstance(keyword_name, str)
                assert isinstance(keyword_info, dict)
                assert "doc" in keyword_info
                assert isinstance(keyword_info["doc"], str)
                assert "values" in keyword_info
                assert isinstance(keyword_info["values"], list)

    def test_runtyp_values(self):
        """Test RUNTYP has expected values."""
        runtyp = GAMESS_KEYWORDS["CONTRL"]["RUNTYP"]
        values = runtyp["values"]
        assert "ENERGY" in values
        assert "OPTIMIZE" in values
        assert "HESSIAN" in values

    def test_scftyp_values(self):
        """Test SCFTYP has expected values."""
        scftyp = GAMESS_KEYWORDS["CONTRL"]["SCFTYP"]
        values = scftyp["values"]
        assert "RHF" in values
        assert "UHF" in values
        assert "ROHF" in values

    def test_system_keywords(self):
        """Test SYSTEM keywords exist."""
        assert "SYSTEM" in GAMESS_KEYWORDS
        system = GAMESS_KEYWORDS["SYSTEM"]
        assert "MWORDS" in system
        assert "MEMDDI" in system

    def test_dft_keywords(self):
        """Test DFT keywords exist."""
        assert "DFT" in GAMESS_KEYWORDS
        dft = GAMESS_KEYWORDS["DFT"]
        assert "METHOD" in dft
        assert "NRAD" in dft

    def test_statpt_keywords(self):
        """Test STATPT keywords exist."""
        assert "STATPT" in GAMESS_KEYWORDS
        statpt = GAMESS_KEYWORDS["STATPT"]
        assert "OPTTOL" in statpt
        assert "NSTEP" in statpt

    def test_force_keywords(self):
        """Test FORCE keywords exist."""
        assert "FORCE" in GAMESS_KEYWORDS
        force = GAMESS_KEYWORDS["FORCE"]
        assert "VIBANL" in force
        assert "TEMP" in force
