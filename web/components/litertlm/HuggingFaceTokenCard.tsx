"use client";

import { useEffect, useState } from "react";
import { Eye, EyeOff, Key, Loader2, Save } from "lucide-react";
import { apiFetch, apiUrl } from "@/lib/api";

export default function HuggingFaceTokenCard() {
  const [token, setToken] = useState("");
  const [maskedToken, setMaskedToken] = useState("");
  const [showToken, setShowToken] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: "", text: "" });

  useEffect(() => {
    async function loadToken() {
      try {
        const res = await apiFetch(apiUrl("/api/v1/litertlm/models/token"));
        if (res.ok) {
          const data = await res.json();
          if (data.has_token) {
            setMaskedToken(data.masked_token);
          }
        }
      } catch (err) {
        console.error("Failed to load HF token:", err);
      } finally {
        setLoading(false);
      }
    }
    loadToken();
  }, []);

  const handleSave = async () => {
    if (!token.trim()) return;
    setSaving(true);
    setMessage({ type: "", text: "" });
    try {
      const res = await apiFetch(apiUrl("/api/v1/litertlm/models/token"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: token.trim() }),
      });
      if (res.ok) {
        setMessage({ type: "success", text: "Token saved successfully" });
        setMaskedToken(`${token.slice(0, 4)}...${token.slice(-4)}`);
        setToken("");
        setShowToken(false);
      } else {
        const error = await res.json();
        setMessage({ type: "error", text: error.detail || "Failed to save token" });
      }
    } catch (err) {
      setMessage({ type: "error", text: "Network error saving token" });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="rounded-xl border border-[var(--border)] p-5">
        <div className="flex animate-pulse items-center gap-3">
          <div className="h-5 w-5 rounded-md bg-[var(--muted)]" />
          <div className="h-4 w-32 rounded-md bg-[var(--muted)]" />
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-[var(--border)] p-5">
      <div className="mb-4">
        <div className="text-[13px] font-medium text-[var(--foreground)] flex items-center gap-2">
          <Key className="h-4 w-4 text-[var(--muted-foreground)]" />
          Access Token
        </div>
        <p className="mt-1 text-[12px] text-[var(--muted-foreground)]">
          Required to download gated models like Gemma or Llama from Hugging Face.
          Create one with Read permissions in your Hugging Face settings.
        </p>
      </div>

      <div className="space-y-4">
        {maskedToken && !showToken && !token && (
          <div className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--muted)]/30 px-3 py-2">
            <div className="flex-1 font-mono text-[13px] text-[var(--foreground)]">
              {maskedToken}
            </div>
            <button
              onClick={() => setShowToken(true)}
              className="text-[11px] font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] underline underline-offset-2"
            >
              Change
            </button>
          </div>
        )}

        {(showToken || !maskedToken || token) && (
          <div className="flex items-center gap-3">
            <div className="relative flex-1">
              <input
                type={showToken ? "text" : "password"}
                autoComplete="new-password"
                spellCheck={false}
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder={maskedToken ? "Enter new token..." : "hf_..."}
                className="w-full rounded-lg border border-[var(--border)] bg-transparent px-3 py-2 pr-10 font-mono text-[13px] text-[var(--foreground)] outline-none transition-colors placeholder:text-[var(--muted-foreground)]/40 focus:border-[var(--ring)]"
              />
              <button
                type="button"
                onClick={() => setShowToken((prev) => !prev)}
                className="absolute right-1 top-1/2 -translate-y-1/2 rounded-md p-1.5 text-[var(--muted-foreground)] hover:bg-[var(--muted)] hover:text-[var(--foreground)]"
              >
                {showToken ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </button>
            </div>
            <button
              onClick={handleSave}
              disabled={!token.trim() || saving}
              className="inline-flex items-center gap-1.5 rounded-lg bg-[var(--foreground)] px-4 py-2 text-[12px] font-medium text-[var(--background)] transition-opacity hover:opacity-80 disabled:opacity-40"
            >
              {saving ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <Save className="h-3.5 w-3.5" />
              )}
              Save
            </button>
          </div>
        )}

        {message.text && (
          <p
            className={`text-[12px] ${
              message.type === "error"
                ? "text-red-500"
                : "text-emerald-500"
            }`}
          >
            {message.text}
          </p>
        )}
      </div>
    </div>
  );
}
