"""Tests for Find References feature."""

import re


class TestReferencesLogic:
    """Tests for find references logic."""

    def test_references_finds_group_occurrences(self):
        """Test finding all group occurrences."""
        content = """! Test file
$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
$SYSTEM MWORDS=100 $END
$CONTRL SCFTYP=UHF $END
"""
        word_upper = "CONTRL"
        lines = content.split("\n")

        locations = []
        for i, line_content in enumerate(lines):
            if re.search(rf"\${word_upper}\b", line_content, re.IGNORECASE):
                locations.append((i, line_content))

        assert len(locations) == 2  # Two $CONTRL occurrences

    def test_references_finds_keyword_occurrences(self):
        """Test finding all keyword occurrences."""
        content = """! Test file
$CONTRL SCFTYP=RHF RUNTYP=ENERGY $END
$SYSTEM MWORDS=100 $END
$CONTRL SCFTYP=UHF $END
"""
        word_upper = "SCFTYP"
        lines = content.split("\n")

        locations = []
        for i, line_content in enumerate(lines):
            if re.search(rf"\b{word_upper}\s*=", line_content, re.IGNORECASE):
                locations.append((i, line_content))

        assert len(locations) == 2  # Two SCFTYP= occurrences

    def test_references_no_match(self):
        """Test with no matching word."""
        content = """! Test file
$CONTRL SCFTYP=RHF $END
"""
        word_upper = "NONEXISTENT"
        lines = content.split("\n")

        locations = []
        for i, line_content in enumerate(lines):
            if re.search(rf"\${word_upper}\b", line_content, re.IGNORECASE):
                locations.append((i, line_content))

        assert len(locations) == 0
