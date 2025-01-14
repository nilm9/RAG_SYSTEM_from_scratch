from rag_project.core.pipeline import PipelineSingleton

if __name__ == "__main__":
    pipeline = PipelineSingleton()
    pipeline.run_retrieval()
