from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """all messages are in Vietnamese.
            You are a helpful assistant that translates English to Vietnamese.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)