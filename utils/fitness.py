class FitnessEvaluator:
    """
    Evaluates the fitness of a chord sequence based on various musical criteria.

    Attributes:
        melody (list): List of tuples representing notes as (pitch, duration).
        chords (dict): Dictionary of chords with their corresponding notes.
        weights (dict): Weights for different fitness evaluation functions.
        preferred_transitions (dict): Preferred chord transitions.
    """

    def __init__(
        self, melody_data, chord_mappings, weights, preferred_transitions
    ):
        """
        Initialize the FitnessEvaluator with melody, chords, weights, and
        preferred transitions.

        Parameters:
            melody_data (MelodyData): Melody information.
            chord_mappings (dict): Available chords mapped to their notes.
            weights (dict): Weights for each fitness evaluation function.
            preferred_transitions (dict): Preferred chord transitions.
        """
        self.melody_data = melody_data
        self.chord_mappings = chord_mappings
        self.weights = weights
        self.preferred_transitions = preferred_transitions

    def get_chord_sequence_with_highest_fitness(self, chord_sequences):
        """
        Returns the chord sequence with the highest fitness score.

        Parameters:
            chord_sequences (list): List of chord sequences to evaluate.

        Returns:
            list: Chord sequence with the highest fitness score.
        """
        return max(chord_sequences, key=self.evaluate)

    def evaluate(self, chord_sequence):
        """
        Evaluate the fitness of a given chord sequence.

        Parameters:
            chord_sequence (list): The chord sequence to evaluate.

        Returns:
            float: The overall fitness score of the chord sequence.
        """
        return sum(
            self.weights[func] * getattr(self, f"_{func}")(chord_sequence)
            for func in self.weights
        )

    def _chord_melody_congruence(self, chord_sequence):
        """
        Calculates the congruence between the chord sequence and the melody.
        This function assesses how well each chord in the sequence aligns
        with the corresponding segment of the melody. The alignment is
        measured by checking if the notes in the melody are present in the
        chords being played at the same time, rewarding sequences where the
        melody notes fit well with the chords.

        Parameters:
            chord_sequence (list): A list of chords to be evaluated against the
                melody.

        Returns:
            float: A score representing the degree of congruence between the
                chord sequence and the melody, normalized by the melody's
                duration.
        """
        score, melody_index = 0, 0
        for chord in chord_sequence:
            bar_duration = 0
            while bar_duration < 4 and melody_index < len(
                self.melody_data.notes
            ):
                pitch, duration = self.melody_data.notes[melody_index]
                if pitch[0] in self.chord_mappings[chord]:
                    score += duration
                bar_duration += duration
                melody_index += 1
        return score / self.melody_data.duration

    def _chord_variety(self, chord_sequence):
        """
        Evaluates the diversity of chords used in the sequence. This function
        calculates a score based on the number of unique chords present in the
        sequence compared to the total available chords. Higher variety in the
        chord sequence results in a higher score, promoting musical
        complexity and interest.

        Parameters:
            chord_sequence (list): The chord sequence to evaluate.

        Returns:
            float: A normalized score representing the variety of chords in the
                sequence relative to the total number of available chords.
        """
        unique_chords = len(set(chord_sequence))
        total_chords = len(self.chord_mappings)
        return unique_chords / total_chords

    def _harmonic_flow(self, chord_sequence):
        """
        Assesses the harmonic flow of the chord sequence by examining the
        transitions between successive chords. This function scores the
        sequence based on how frequently the chord transitions align with
        predefined preferred transitions. Smooth and musically pleasant
        transitions result in a higher score.

        Just to my taste, I added a bunch of preferred transitions that I like.

        Parameters:
            chord_sequence (list): The chord sequence to evaluate.

        Returns:
            float: A normalized score based on the frequency of preferred chord
                transitions in the sequence.
        """
        score = 0
        for i in range(len(chord_sequence) - 1):
            next_chord = chord_sequence[i + 1]
            if next_chord in self.preferred_transitions[chord_sequence[i]]:
                score += 1
        return score / (len(chord_sequence) - 1)

    def _functional_harmony(self, chord_sequence):
        """
        Evaluates the chord sequence based on principles of functional harmony.
        This function checks for the presence of the 2-5-1 progression. This makes it more jazzy.

        Parameters:
            chord_sequence (list): The chord sequence to evaluate.

        Returns:
            float: A score representing the extent to which the sequence
                adheres to traditional functional harmony, normalized by
                the number of checks performed.
        """
        score = 0
        # Check for tonic at the beginning and end
        if chord_sequence[0] in ["C"]:
            score += 1
        if chord_sequence[-1] in ["C"]:
            score += 1

        # Check if 2 5 1 is present
        bigram_model = {
            "G7": ["CMaj7"],
            "D7": ["G7"],
            "CMaj7": ["D7"],
        }

        for i in range(len(chord_sequence) - 1):
            current_chord = chord_sequence[i]
            next_chord = chord_sequence[i + 1]
            if current_chord in bigram_model.keys():
                if next_chord in bigram_model.get(current_chord, []):
                    score += 1

        # also start with a tonic chord and end with a tonic chord
        if chord_sequence[0] not in ["CMaj7"] or chord_sequence[-1] not in ["CMaj7"]:
            score -= 10

        # Normalize score by the number of checks performed
        return score / (len(chord_sequence) + 2)

    def _tension(self, chord_sequence):
        """
        Evaluate the presents of tension chords in the chord sequence.
        Tension introduces dissonance and instability, making it moody and interesting.

        Parameters:
            chord_sequence (list): The chord sequence to evaluate.

        Returns:
            float: A score representing the extent to which the sequence
                contains chords that create tension, normalized by the number
                of chords in the sequence.
        """
        tension_chords = ["E7", "G7", "BminMaj7b5", "Fsus2", "Fmin6"]
        score = sum(1 for chord in chord_sequence if chord in tension_chords)
        return score / len(chord_sequence)

    def _parallel_fifths(self, chord_sequence):
        """
        Evaluate the presence of parallel fifths in the chord sequence.
        Parallel fifths are considered poor voice leading and are generally avoided in traditional harmony.

        Parameters:
            chord_sequence (list): The chord sequence to evaluate.

        Returns:
            float: A score representing the extent to which the sequence
                contains parallel fifths, normalized by the number of chord
                transitions checked.
        """
        parallel_fifths = 0
        for i in range(len(chord_sequence) - 1):
            current_chord = chord_sequence[i]
            next_chord = chord_sequence[i + 1]
            if current_chord in ["CMaj7", "G7"] and next_chord in ["CMaj7", "G7"]:
                parallel_fifths += 1
            if current_chord in ["Am7add11", "E7"] and next_chord in ["Am7add11", "E7"]:
                parallel_fifths += 1
            if current_chord in ["D7", "Am7add11"] and next_chord in ["D7", "Am7add11"]:
                parallel_fifths += 1
            if current_chord in ["E7", "BminMaj7b5"] and next_chord in ["E7", "BminMaj7b5"]:
                parallel_fifths += 1
            if current_chord in ["Fsus2", "CMaj7"] and next_chord in ["Fsus2", "CMaj7"]:
                parallel_fifths += 1
                if current_chord in ["Fmin6", "CMaj7"] and next_chord in ["Fmin6", "CMaj7"]:
                    parallel_fifths += 1
            if current_chord in ["G7", "D7"] and next_chord in ["G7", "D7"]:
                parallel_fifths += 1

        score = 1 - (parallel_fifths / len(chord_sequence))

        return score
