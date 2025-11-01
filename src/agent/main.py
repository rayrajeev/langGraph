from concurrent.futures import thread
import os
import sys
from typing import Annotated

from graph import graph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState


# ANSI color codes for terminal output
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def print_banner():
    """Print a colorful welcome banner."""
    banner = f"""
{Colors.BRIGHT_MAGENTA}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              🤖 Welcome to LangGraph Agent Chat! 🚀                          ║
║                                                                               ║
║         🎯 I can help you with calculations and conversations                 ║
║         💡 Try asking me to multiply numbers!                                 ║
║         🚪 Type 'quit', 'exit', or 'q' to leave                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)


def print_separator():
    """Print a colorful separator line."""
    print(f"{Colors.BRIGHT_CYAN}{'═' * 79}{Colors.ENDC}")


def print_user_prompt():
    """Print a colorful user input prompt."""
    return f"{Colors.BRIGHT_GREEN}{Colors.BOLD}👤 You: {Colors.ENDC}"


def print_agent_response(content):
    """Print agent response with colors and emojis."""
    print(
        f"{Colors.BRIGHT_BLUE}{Colors.BOLD}🤖 Agent:{Colors.ENDC} {Colors.BRIGHT_WHITE}{content}{Colors.ENDC}"
    )


def print_error(error_msg):
    """Print error message with red color and emoji."""
    print(
        f"{Colors.BRIGHT_RED}{Colors.BOLD}❌ Error:{Colors.ENDC} {Colors.BRIGHT_RED}{error_msg}{Colors.ENDC}"
    )
    print(f"{Colors.BRIGHT_YELLOW}💡 Please try again!{Colors.ENDC}")


def print_goodbye():
    """Print a colorful goodbye message."""
    goodbye = f"""
{Colors.BRIGHT_MAGENTA}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                  👋 Thank you for using LangGraph!                           ║
║                           🌟 Goodbye! 🌟                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(goodbye)


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def main():
    """Main function that creates a chat-like interface using the graph."""
    # Clear screen and show banner
    clear_screen()
    print_banner()
    print_separator()

    # Initialize the conversation state
    state = MessagesState(messages=[])
    # Message counter for conversation tracking
    message_count = 0
    thread_id = int(input("Enter a thread ID to continue: ").strip())
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    while True:
        # Get user input with colorful prompt
        user_input = input(print_user_prompt()).strip()

        # Check for exit conditions
        if user_input.lower() in ["quit", "exit", "q"]:
            print_goodbye()
            break
        if not user_input:
            print(f"{Colors.BRIGHT_YELLOW}💬 Please enter a message!{Colors.ENDC}")
            continue

        # Add user message to state
        state["messages"] = [HumanMessage(user_input)]
        message_count += 1

        try:
            # Show processing indicator
            print(f"{Colors.BRIGHT_CYAN}🔄 Processing your request...{Colors.ENDC}")

            # Run the graph with the current state
            result = graph.invoke(state, config=config)

            # Get the last message from the result
            if result["messages"]:
                last_message = result["messages"][-1]

                if isinstance(last_message, AIMessage):
                    print_agent_response(last_message.content)
                else:
                    print_agent_response(last_message.content)

                # Update state with all messages from the result
                state["messages"] = result["messages"]

                # Show conversation stats
                print(
                    f"{Colors.BRIGHT_CYAN}💬 Messages exchanged: {message_count}{Colors.ENDC}"
                )
            else:
                print_error("I'm sorry, I couldn't process that request.")

        except Exception as e:
            print_error(str(e))

        # Add a separator between conversations
        print(f"{Colors.BRIGHT_CYAN}{'─' * 60}{Colors.ENDC}")


if __name__ == "__main__":
    main()
