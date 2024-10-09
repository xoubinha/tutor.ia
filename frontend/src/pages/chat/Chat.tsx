import { useRef, useState, useEffect } from "react";
import { Stack } from "@fluentui/react";
import {
  BroomRegular,
  DismissRegular,
  SquareRegular,
} from "@fluentui/react-icons";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { v4 as uuidv4 } from "uuid";

import styles from "./Chat.module.css";
import TutoriaLogo from "../../assets/tutoria_logo.png";

import {
  ChatMessage,
  ConversationRequest,
  callConversationApi,
  Citation,
  ToolMessageContent,
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";

const Chat = () => {
  const lastQuestionRef = useRef<string>("");
  const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [showLoadingMessage, setShowLoadingMessage] = useState<boolean>(false);
  const [activeCitation, setActiveCitation] =
    useState<
      [
        content: string,
        id: string,
        title: string,
        filepath: string,
        url: string,
        metadata: string
      ]
    >();
  const [isCitationPanelOpen, setIsCitationPanelOpen] =
    useState<boolean>(false);
  const [answers, setAnswers] = useState<ChatMessage[]>([]);
  const abortFuncs = useRef([] as AbortController[]);
  const [conversationId, setConversationId] = useState<string>(uuidv4());
  const makeApiRequest = async (question: string) => {
    lastQuestionRef.current = question;

    setIsLoading(true);
    setShowLoadingMessage(true);
    const abortController = new AbortController();
    abortFuncs.current.unshift(abortController);

    const userMessage: ChatMessage = {
      role: "user",
      content: question,
    };

    const request: ConversationRequest = {
      id: conversationId,
      messages: [...answers, userMessage],
    };
    try {
      const response = await callConversationApi(
        request,
        abortController.signal
      );
      console.log("Response:", response); // Log the response object
      if (response.ok){
        const responseBody = await response.json(); // Parse the response body as JSON
        console.log("Response Body:", responseBody.response); // Log the response body
        setShowLoadingMessage(false);
        if (responseBody.error) {
          setAnswers([
            ...answers,
            userMessage,
            { role: "error", content: responseBody.error },
          ]);
        } else {
          setAnswers([
            ...answers,
            userMessage,
            { role: "assistant", content: responseBody.response },
          ]);
        }
      } else {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData.error));
      }
    } catch (error) {
      console.error("Fetch error:", error); // Log fetch errors
      setAnswers([
        ...answers,
        userMessage,
        { role: "error", content: "An error occurred while fetching the response." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };
      // if (response?.body) {
      //   const reader = response.body.getReader();
      //   let runningText = "";
      //   while (true) {
      //     const { done, value } = await reader.read();
      //     if (done) break;

      //     var text = new TextDecoder("utf-8").decode(value);
      //     const objects = text.split("\n");
      //     objects.forEach((obj) => {
      //       try {
      //         runningText += obj;
      //         result = JSON.parse(runningText);
      //         setShowLoadingMessage(false);
      //         if (result.error) {
      //           setAnswers([
      //             ...answers,
      //             userMessage,
      //             { role: "error", content: result.error },
      //           ]);
      //         } else {
      //           setAnswers([
      //             ...answers,
      //             userMessage,
      //             ...result.choices[0].messages,
      //           ]);
      //         }
      //         runningText = "";
      //       } catch { }
      //     });
      //   }
      //   setAnswers([...answers, userMessage, ...result.choices[0].messages]);
      // }
  //   } catch (e) {
  //     if (!abortController.signal.aborted) {
  //       if (e instanceof Error) {
  //         console.log("Entra aqui")
  //         alert(e.message);
  //       }
  //       else {
  //         alert('An error occurred. Please try again. If the problem persists, please contact the site administrator.');
  //       }
  //     }
  //     setAnswers([...answers, userMessage]);
  //   } finally {
  //     setIsLoading(false);
  //     setShowLoadingMessage(false);
  //     abortFuncs.current = abortFuncs.current.filter(
  //       (a) => a !== abortController
  //     );
  //   }

  //   return abortController.abort();
  // };


  const clearChat = () => {
    lastQuestionRef.current = "";
    setActiveCitation(undefined);
    setAnswers([]);
    setConversationId(uuidv4());
  };

  const stopGenerating = () => {
    abortFuncs.current.forEach((a) => a.abort());
    setShowLoadingMessage(false);
    setIsLoading(false);
  };

  useEffect(
    () => chatMessageStreamEnd.current?.scrollIntoView({ behavior: "smooth" }),
    [showLoadingMessage]
  );

  const onShowCitation = (citation: Citation) => {
    setActiveCitation([
      citation.content,
      citation.id,
      citation.title ?? "",
      citation.filepath ?? "",
      "",
      "",
    ]);
    setIsCitationPanelOpen(true);
  };

  const parseCitationFromMessage = (message: ChatMessage) => {
    if (message.role === "tool") {
      try {
        const toolMessage = JSON.parse(message.content) as ToolMessageContent;
        return toolMessage.citations;
      } catch {
        return [];
      }
    }
    return [];
  };

  return (
    <div className={styles.container}>
      <Stack horizontal className={styles.chatRoot}>
        <div className={`${styles.chatContainer} ${styles.MobileChatContainer}`}>
          {!lastQuestionRef.current ? (
            <Stack className={styles.chatEmptyState}>
              <img src={TutoriaLogo} className={styles.chatIcon} aria-hidden="true" alt="Tutor.ia logo"/>
              <h1 className={styles.chatEmptyStateTitle}>¡Hola, soy Tutor.ia!</h1>
              <h2 className={styles.chatEmptyStateSubtitle}>
                Estoy aquí para ayudarte con tu estudio. Hazme una pregunta y te responderé lo mejor que pueda.
              </h2>
            </Stack>
          ) : (
            <div
              className={styles.chatMessageStream}
              style={{ marginBottom: isLoading ? "40px" : "0px" }}
            >
              {answers.map((answer, index) => (
                 <div key={index}>
                  {answer.role === "user" ? (
                    <div className={styles.chatMessageUser}>
                      <div className={styles.chatMessageUserMessage}>
                        {answer.content}
                      </div>
                    </div>
                  ) : answer.role === "assistant" || answer.role === "error" ? (
                    <div className={styles.chatMessageGpt}>
                      <Answer
                        answer={{
                          answer:
                            answer.role === "assistant"
                              ? answer.content
                              : "Sorry, an error occurred. Try refreshing the conversation or waiting a few minutes. If the issue persists, contact your system administrator. Error: " +
                              answer.content,
                          citations:
                            answer.role === "assistant"
                              ? parseCitationFromMessage(answers[index - 1])
                              : [],
                        }}
                        onCitationClicked={(c) => onShowCitation(c)}
                        index={index}
                      />
                    </div>
                  ) : null}
                </div>
              ))}
              {showLoadingMessage && (
                <>
                  <div className={styles.chatMessageUser}>
                    <div className={styles.chatMessageUserMessage}>
                      {lastQuestionRef.current}
                    </div>
                  </div>
                  <div className={styles.chatMessageGpt}>
                    <Answer
                      answer={{
                        answer: "Generating answer...",
                        citations: [],
                      }}
                      onCitationClicked={() => null}
                      index={0}
                    />
                  </div>
                </>
              )}
              <div ref={chatMessageStreamEnd} />
            </div>
          )}

          <Stack horizontal className={styles.chatInput}>
            {isLoading && (
              <Stack
                horizontal
                className={styles.stopGeneratingContainer}
                role="button"
                aria-label="Stop generating"
                tabIndex={0}
                onClick={stopGenerating}
                onKeyDown={(e) =>
                  e.key === "Enter" || e.key === " " ? stopGenerating() : null
                }
              >
                <SquareRegular
                  className={styles.stopGeneratingIcon}
                  aria-hidden="true"
                />
                <span className={styles.stopGeneratingText} aria-hidden="true">
                  Stop generating
                </span>
              </Stack>
            )}
            <BroomRegular
              className={`${styles.clearChatBroom} ${styles.mobileclearChatBroom}`}
              style={{
                background:
                  isLoading || answers.length === 0
                    ? "#BDBDBD"
                    : "#252d58",
                cursor: isLoading || answers.length === 0 ? "" : "pointer",
              }}
              onClick={clearChat}
              onKeyDown={(e) =>
                e.key === "Enter" || e.key === " " ? clearChat() : null
              }
              aria-label="Clear session"
              role="button"
              tabIndex={0}
            />
            <QuestionInput
              clearOnSend
              placeholder="Escribe tu pregunta..."
              disabled={isLoading}
              onSend={(question) => makeApiRequest(question)}
            />
          </Stack>
        </div>
        {answers.length > 0 && isCitationPanelOpen && activeCitation && (
          <Stack.Item className={`${styles.citationPanel} ${styles.mobileStyles}`}>
            <Stack
              horizontal
              className={styles.citationPanelHeaderContainer}
              horizontalAlign="space-between"
              verticalAlign="center"
            >
              <span className={styles.citationPanelHeader}>Citations</span>
              <DismissRegular
                className={styles.citationPanelDismiss}
                onClick={() => setIsCitationPanelOpen(false)}
              />
            </Stack>
            <h5 className={`${styles.citationPanelTitle} ${styles.mobileCitationPanelTitle}`}>{activeCitation[2]}</h5>
            <ReactMarkdown
              className={`${styles.citationPanelContent} ${styles.mobileCitationPanelContent}`}
              children={activeCitation[0]}
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            />
          </Stack.Item>
        )}
      </Stack>
    </div>
  );
};

export default Chat;
