from patrim.pdf import read_text

TEST_LINE1 = '2016P04788  197//AO/167//10  95  DEUIL LA BARRE  10 ALL CANTI  18/07/2016  1959  6  450 000  0  164  2743,90'
TEST_LINE2 = '2015P02931  210//AD/6//  95  ENGHIEN LES BAINS  19 BD D\'ORMESSON  03/06/2015  1900  5  700 000  665  160  4375,00'

def test__parse_line():
    for line in [TEST_LINE1, TEST_LINE2]:
        df = read_text(line)

        assert 'CAD' in df.columns
        assert 'PRIX' in df.columns
        assert 'ADRESSE' in df.columns
        assert 'LATITUDE' not in df.columns

        assert not df.empty
