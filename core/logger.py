"""Logging and tracing mechanism for agent inputs, tool calls, outputs."""
import logging
import json
from datetime import datetime
from pathlib import Path

# Setup file logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"agent_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)

def log_agent_input(agent_name: str, input_data: dict):
    logging.info(f"AGENT_INPUT | {agent_name} | {json.dumps(input_data, default=str)}")

def log_tool_call(agent_name: str, tool_name: str, args: dict, result: str):
    logging.info(f"TOOL_CALL | {agent_name} | {tool_name} | args={json.dumps(args, default=str)} | result_preview={result[:200]}")

def log_agent_output(agent_name: str, output: dict):
    logging.info(f"AGENT_OUTPUT | {agent_name} | {json.dumps(output, default=str)}")

def log_error(agent_name: str, error: str):
    logging.error(f"ERROR | {agent_name} | {error}")