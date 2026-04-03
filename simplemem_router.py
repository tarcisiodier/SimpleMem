"""
SimpleMem — Unified Entry Point

Routes between single-modal (text) and multi-modal (omni) memory systems.

Usage:
    import simplemem_router as simplemem

    # Text-only mode (lightweight, single-modal)
    mem = simplemem.create(mode="text", clear_db=True)
    mem.add_dialogue("Alice", "Let's meet at 2pm", "2025-11-15T14:30:00")
    mem.finalize()
    answer = mem.ask("When will they meet?")

    # Multimodal mode (text, image, audio, video)
    mem = simplemem.create(mode="omni", data_dir="./my_memory")
    mem.add_text("User loves hiking.", tags=["session_id:D1"])
    result = mem.query("What does the user enjoy?", top_k=5)
    mem.close()
"""

import os
import sys


def create(mode="text", **kwargs):
    """
    Create a SimpleMem instance.

    Args:
        mode: "text" for single-modal (SimpleMem),
              "omni" for multimodal (Omni-SimpleMem)
        **kwargs: passed to the underlying system constructor

    Returns:
        SimpleMemSystem   when mode="text"
        OmniMemoryOrchestrator  when mode="omni"
    """
    if mode == "text":
        from main import SimpleMemSystem
        return SimpleMemSystem(**kwargs)

    elif mode == "omni":
        omni_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OmniSimpleMem")
        if omni_path not in sys.path:
            sys.path.insert(0, omni_path)
        from omni_memory import OmniMemoryOrchestrator, OmniMemoryConfig
        config = kwargs.pop("config", None) or OmniMemoryConfig()
        return OmniMemoryOrchestrator(config=config, **kwargs)

    else:
        raise ValueError(
            f"Unknown mode: {mode!r}. Use 'text' (single-modal) or 'omni' (multimodal)."
        )
