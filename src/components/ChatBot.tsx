"use client";
import { useState } from "react";
import ChatInput from "./ChatInput";
import ChatMessages from "./ChatMessages";

export default function ChatBot() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>(
    []
  );
  const [loading, setLoading] = useState(false);

  const handleSend = async (userMessage: string) => {
    setMessages((msgs) => [...msgs, { role: "user", content: userMessage }]);
    setLoading(true);

    let botMessage = "";
    setMessages((msgs) => [...msgs, { role: "bot", content: "" }]);

    const response = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ scenario: userMessage }),
      headers: { "Content-Type": "application/json" },
    });

    if (response.body) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunk = decoder.decode(value);
          botMessage += chunk;
          setMessages((msgs) =>
            msgs.map((msg, i) =>
              i === msgs.length - 1 && msg.role === "bot"
                ? { ...msg, content: botMessage }
                : msg
            )
          );
        }
      }
    }
    setLoading(false);
  };

  return (
    <div 
    className="flex flex-col h-[100vh] md:h-[90vh] w-full max-w-3xl rounded-2xl shadow-xl bg-[var(--background)] border border-[var(--input-border)] p-4 md:p-6 transition-all"
    >
      <h1 className="text-2xl font-semibold mb-4 text-center text-[var(--foreground)]">
        Insight Fusion
      </h1>
      <div className="flex-1 overflow-y-auto mb-2">
        <ChatMessages messages={messages} />
      </div>
      <ChatInput onSend={handleSend} loading={loading} />
    </div>
  );
}
