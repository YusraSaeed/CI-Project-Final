import { useState, useEffect, useRef } from "react";
import { Moon, Sun, Check, Send, ChevronDown, BotIcon as Robot, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import ReactMarkdown from "react-markdown";

function adjustColor(color, amount) {
  const hex = color.replace("#", "");
  const num = parseInt(hex, 16);
  const r = Math.min(255, Math.max(0, (num >> 16) + amount * 255));
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0x00ff) + amount * 255));
  const b = Math.min(255, Math.max(0, (num & 0x0000ff) + amount * 255));
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

const ACCENT_COLORS = [
  { name: "purple", value: "#7C3AED" },
  { name: "violet", value: "#8B5CF6" },
  { name: "red", value: "#EF4444" },
  { name: "orange", value: "#F97316" },
  { name: "yellow", value: "#EAB308" },
  { name: "green", value: "#10B981" },
  { name: "blue", value: "#3B82F6" },
  { name: "gradient", value: "linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)" },
];

const FONT_SIZES = [
  { name: "Small", value: "14px" },
  { name: "Medium", value: "16px" },
  { name: "Large", value: "18px" },
  { name: "Extra Large", value: "20px" },
];

export default function ChatCustomizer() {
  const [theme, setTheme] = useState("light");
  const [messages, setMessages] = useState([]);
  const [accentColor, setAccentColor] = useState(ACCENT_COLORS[0].value);
  const [fontSize, setFontSize] = useState(FONT_SIZES[1].value); // Default to Medium
  const [isTyping, setIsTyping] = useState(false);

  const chatContainerRef = useRef(null);

  useEffect(() => {
    setMessages([{
      type: "bot",
      content: "Hi, I'm TechBot, your laptop expert! 💻🔍\nI can help you find the best laptop or answer your tech-related questions. How can I assist you today?",
    }]);
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (input) => {
    if (!input.trim()) return;

    const newUserMessage = { type: "user", content: input };
    setMessages((prev) => [...prev, newUserMessage]);
    setIsTyping(true);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input, stream: false }),
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        const newBotMessage = { type: "bot", content: data.response };
        setMessages((prev) => [...prev, newBotMessage]);
      } else {
        const errorText = await response.text();
        console.error("API Error:", errorText);
        const errorMessage = { type: "bot", content: `Error: ${errorText}` };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error("Network Error:", error);
      const errorMessage = { type: "bot", content: "Sorry, there was a network error. Please try again later." };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setIsTyping(false);
  };

  return (
    <div className="min-h-screen flex">
      {/* Sidebar Panel */}
      <div
        className="w-1/6 bg-gray-200 p-4 flex flex-col space-y-8"
        style={{
          minHeight: "100vh",
          backgroundColor: theme === "dark" ? "#2D3748" : "#E5E7EB", // Darker sidebar in dark mode
        }}
      >
        <h1 className="text-xl font-bold">Customize TechBot</h1>

        <div>
          <h2 className="text-lg mb-2">Theme</h2>
          <div className="flex gap-4">
            <Button
              variant={theme === "light" ? "default" : "outline"}
              className={cn(
                "h-12 w-20 flex-col gap-1",
                theme === "light" && "ring-2 ring-offset-2",
                theme === "light" && "ring-[#7C3AED]"
              )}
              onClick={() => setTheme("light")}
            >
              <Sun className="h-5 w-5" />
              <span>Light</span>
            </Button>
            <Button
              variant={theme === "dark" ? "default" : "outline"}
              className={cn(
                "h-12 w-20 flex-col gap-1",
                theme === "dark" && "ring-2 ring-offset-2",
                theme === "dark" && "ring-[#7C3AED]"
              )}
              onClick={() => setTheme("dark")}
            >
              <Moon className="h-5 w-5" />
              <span>Dark</span>
            </Button>
          </div>
        </div>

        <div>
          <h2 className="text-lg mb-2">Accent Color</h2>
          <div className="flex flex-wrap gap-2">
            {ACCENT_COLORS.map((color) => (
              <button
                key={color.name}
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center",
                  "ring-2 ring-offset-2 transition-all",
                  accentColor === color.value
                    ? "ring-[#7C3AED]"
                    : "ring-transparent"
                )}
                style={{ background: color.value }}
                onClick={() => setAccentColor(color.value)}
              >
                {accentColor === color.value && (
                  <Check className="h-4 w-4 text-white" />
                )}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-lg mb-2">Font Size</h2>
          <div className="flex flex-wrap gap-2">
            {FONT_SIZES.map((size) => (
              <button
                key={size.name}
                className={cn(
                  "px-3 py-1 rounded border",
                  fontSize === size.value
                    ? "bg-[#7C3AED] text-white"
                    : "bg-white text-gray-700 border-gray-300"
                )}
                onClick={() => setFontSize(size.value)}
              >
                {size.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chat Section */}
      <div
        className="w-full flex flex-col items-center"
        style={{
          backgroundColor: theme === "dark" ? "#1a202c" : "#f7fafc",
          paddingLeft: "10%",
          paddingRight: "10%",
          paddingTop: "2%",
          paddingBottom: "1%",
          height: "100vh",
        }}
      >
        <div
          className="flex-grow w-full overflow-y-auto space-y-4"
          ref={chatContainerRef}
          style={{
            padding: "4px",
            border: "null",
            borderRadius: "4px",
            marginBottom: "4px",
          }}
        >
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className="rounded-lg p-3 max-w-[80%] text-white"
                style={{
                  backgroundColor:
                    message.type === "user"
                      ? adjustColor(accentColor, theme === "dark" ? 0.2 : -0.2)
                      : accentColor,
                  fontSize: fontSize,
                }}
              >
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          ))}
          {isTyping && <div className="text-gray-500 italic">Bot is typing...</div>}
        </div>

        <div className="w-full flex items-center gap-2 px-4">
          <input
            type="text"
            placeholder="Enter your use case here..."
            className="flex-grow border rounded-lg p-2 focus:outline-none"
            style={{
              backgroundColor: theme === "dark" ? "#2D3748" : "#E2E8F0", // Darker input box in dark mode
              color: theme === "dark" ? "#F7FAFC" : "#2D3748", // Text color for dark mode
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && e.target.value.trim()) {
                handleSend(e.target.value.trim());
                e.target.value = "";
              }
            }}
          />
          <Button
            size="icon"
            className="rounded-full"
            style={{ backgroundColor: accentColor }}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
