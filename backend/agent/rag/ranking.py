class ChunkRanker:

    def rank(
        self,
        chunks,
    ):

        return sorted(
            chunks,
            key=lambda chunk: (
                chunk.metadata.get(
                    "score",
                    0.0,
                )
            ),
            reverse=True,
        )