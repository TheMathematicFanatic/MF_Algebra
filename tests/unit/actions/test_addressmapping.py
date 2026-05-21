from conftest import *


puzzle_admap_A = [
	['1', '01'],
	['1', '11'],
	['00', '00'],
	['01', '10']
]


@MFparam('address, addressmap, result', [

	('admap1', '12', [['123', '999']], {'99'}),

	('admap2', '123', [['12', '88'], ['1', '5']], {'883', '523'}),

	('admap3', '12', [['1', []]], None),

	('puzzleA1', '1', puzzle_admap_A, {'01', '11'}),

	('puzzleA2', '0', puzzle_admap_A, None), # Hmm what should this output...

	('puzzleA3', '00', puzzle_admap_A, {'00'}),

	('puzzleA4', '01', puzzle_admap_A, {'10'}),

	('puzzleA5', '01315', puzzle_admap_A, {'10315'}),

	('puzzleA6', '1315', puzzle_admap_A, {'01315', '11315'}),

	('puzzleA7', '315', puzzle_admap_A, {'315'}), # Hm.

])
def test_apply_addressmap(address, addressmap, result):
	assert apply_addressmap(address, addressmap) == result

