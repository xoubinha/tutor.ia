import { ConversationRequest } from "./models";


export async function callConversationApi(options: ConversationRequest, abortSignal: AbortSignal): Promise<Response> {
    const messages = options.messages
    const prompt = messages[messages.length - 1].content;

    const response = await fetch("/conversation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify({
            prompt: prompt,
            conversation_id: options.id
        }),
        signal: abortSignal
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData.error));
    }
    return response;
}
