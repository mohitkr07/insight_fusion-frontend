import { useState } from "react";

export default function ChatInput({
  onSend,
  loading,
}: {
  onSend: (msg: string) => void;
  loading: boolean;
}) {
  const [input, setInput] = useState("");
  return (
    <form
      className="flex gap-2 mt-2"
      onSubmit={(e) => {
        e.preventDefault();
        if (input.trim()) {
          onSend(input.trim());
          setInput("");
        }
      }}
    >
      <input
        className="flex-1 rounded-xl px-4 py-2 bg-[var(--input-bg)] border border-[var(--input-border)] text-[var(--foreground)] placeholder:text-gray-400 focus:ring-2 focus:ring-blue-400 outline-none transition"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={loading}
        placeholder="Type your scenario..."
      />
      <button
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-xl shadow transition disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center"
        disabled={loading || !input.trim()}
        type="submit"
        aria-label="Send"
      >
        {loading ? (
          <svg
            className="animate-spin h-5 w-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="white"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="white"
              d="M4 12a8 8 0 018-8v8z"
            />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 19V5m0 0l-7 7m7-7l7 7"
            />
          </svg>
        )}
      </button>
    </form>
  );
}
