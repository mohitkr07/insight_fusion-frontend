
function parseAgentSections(text: string) {
    const regex = /--- (.*?) ---\n?/g;
    let match;
    let lastIndex = 0;
    const sections: { agent: string; text: string }[] = [];
  
    while ((match = regex.exec(text)) !== null) {
      const agent = match[1];
      const start = match.index + match[0].length;
      if (sections.length > 0) {
        sections[sections.length - 1].text = text.slice(lastIndex, match.index).trim();
      }
      sections.push({ agent, text: "" });
      lastIndex = start;
    }
    if (sections.length > 0) {
      sections[sections.length - 1].text = text.slice(lastIndex).trim();
    }
    return sections.length ? sections : [{ agent: "", text }];
  }
  
  export default function ChatMessages({
    messages,
  }: {
    messages: { role: string; content: string }[];
  }) {
    return (
      <div className="flex flex-col gap-4 pb-2">
        {messages.map((msg, idx) =>
          msg.role === "user" ? (
            <div
              key={idx}
              className="flex justify-end"
            >
              <div
                className="max-w-[80%] md:max-w-[70%] px-4 py-2 rounded-2xl shadow-sm text-sm bg-[var(--bubble-user)] text-[var(--bubble-user-text)] rounded-br-sm"
              >
                {msg.content}
              </div>
            </div>
          ) : (
            // Bot message: parse agent sections
            <div key={idx} className="flex justify-start w-full">
              <div className="max-w-[80%] md:max-w-[70%] px-4 py-2 rounded-2xl shadow-sm text-sm bg-[var(--bubble-bot)] text-[var(--bubble-bot-text)] rounded-bl-sm w-full">
                {parseAgentSections(msg.content).map((section, sidx) => (
                  <div key={sidx} className="mb-4">
                    {section.agent && (
                      <div className="font-bold text-green-700 mb-1">
                        {section.agent}
                      </div>
                    )}
                    <pre className="whitespace-pre-wrap">{section.text}</pre>
                  </div>
                ))}
              </div>
            </div>
          )
        )}
      </div>
    );
  }
  