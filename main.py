from utils.data import MelodyData
from utils.fitness import FitnessEvaluator
from utils.genetics import GeneticMelodyHarmonizer

import music21

def create_score(melody, chord_sequence, chord_mappings):
    """
    Create a music21 score with a given melody and chord sequence.

    Args:
        melody (list): A list of tuples representing notes in the format
            (note_name, duration).
        chord_sequence (list): A list of chord names.

    Returns:
        music21.stream.Score: A music score containing the melody and chord
            sequence.
    """
    # Create a Score object
    score = music21.stream.Score()

    # Create the melody part and add notes to it
    melody_part = music21.stream.Part()
    for note_name, duration in melody:
        melody_note = music21.note.Note(note_name, quarterLength=duration)
        melody_part.append(melody_note)

    # Create the chord part and add chords to it
    chord_part = music21.stream.Part()
    current_duration = 0  # Track the duration for chord placement

    for chord_name in chord_sequence:
        # Translate chord names to note lists
        chord_notes_list = chord_mappings.get(chord_name, [])
        # Create a music21 chord
        chord_notes = music21.chord.Chord(
            chord_notes_list, quarterLength=4
        )  # Assuming 4/4 time signature
        chord_notes.offset = current_duration
        chord_part.append(chord_notes)
        current_duration += 4  # Increase by 4 beats

    # Append parts to the score
    score.append(melody_part)
    score.append(chord_part)

    return score


def main():

    twinkle_twinkle_melody = [
        ("C5", 1),
        ("C5", 1),
        ("G5", 1),
        ("G5", 1),
        ("A5", 1),
        ("A5", 1),
        ("G5", 2),  # Twinkle, twinkle, little star,
        ("F5", 1),
        ("F5", 1),
        ("E5", 1),
        ("E5", 1),
        ("D5", 1),
        ("D5", 1),
        ("C5", 2),  # How I wonder what you are!
        ("G5", 1),
        ("G5", 1),
        ("F5", 1),
        ("F5", 1),
        ("E5", 1),
        ("E5", 1),
        ("D5", 2),  # Up above the world so high,
        ("G5", 1),
        ("G5", 1),
        ("F5", 1),
        ("F5", 1),
        ("E5", 1),
        ("E5", 1),
        ("D5", 2),  # Like a diamond in the sky.
        ("C5", 1),
        ("C5", 1),
        ("G5", 1),
        ("G5", 1),
        ("A5", 1),
        ("A5", 1),
        ("G5", 2),  # Twinkle, twinkle, little star,
        ("F5", 1),
        ("F5", 1),
        ("E5", 1),
        ("E5", 1),
        ("D5", 1),
        ("D5", 1),
        ("C5", 2)  # How I wonder what you are!
    ]
    # Modified the weights and chord mappings to fit THE jazz style
    weights = {
        "chord_melody_congruence": 0.5,
        "chord_variety": 0.6,
        "harmonic_flow": 0.3,
        "functional_harmony": 0.6,
        "tension": 0.8,
        "parallel_fifths": 0.4,
    }
    chord_mappings = {
        "CMaj7": ["C", "E", "G", "B"],
        "D7": ["D", "Gb", "A", "C"],
        "E7": ["E", "Ab", "B", "D"],
        "Fsus2": ["F", "G", "A", "C"],
        "Fm6": ["F", "A", "C", "D"],
        "G7": ["G", "B", "D", "F"],
        "Am7add11": ["A", "C", "E", "G", "D"],
        "BminMaj7b5": ["B", "D", "F", "Ab"]
    }
    preferred_transitions = {
        "CMaj7": ["G7", "Am7add11", "Fsus2", "E7", "BminMaj7b5"],
        "D7": ["Fsus2"],
        "E7": ["Am7add11", "Fsus2", "CMaj7", "G7"],
        "Fsus2": ["Fm6"],
        "Fm6": ["CMaj7"],
        "G7": ["Am7add11", "CMaj7"],
        "Am7add11": ["D7", "E7" "Fsus2"],
        "BminMaj7b5": ["CMaj7"]
    }

    # Instantiate objects for generating harmonization
    melody_data = MelodyData(twinkle_twinkle_melody)
    fitness_evaluator = FitnessEvaluator(
        melody_data=melody_data,
        weights=weights,
        chord_mappings=chord_mappings,
        preferred_transitions=preferred_transitions,
    )
    harmonizer = GeneticMelodyHarmonizer(
        melody_data=melody_data,
        chords=list(chord_mappings.keys()),
        population_size=100,
        mutation_rate=0.05,
        fitness_evaluator=fitness_evaluator,
    )

    # Generate chords with genetic algorithm
    generated_chords = harmonizer.generate(generations=1000)

    # Render to music21 score and show it
    music21_score = create_score(
        twinkle_twinkle_melody, generated_chords, chord_mappings
    )
    music21_score.show()

if __name__ == "__main__":
    main()
