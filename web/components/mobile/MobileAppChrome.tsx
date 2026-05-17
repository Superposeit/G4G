"use client";

import Image from "next/image";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  Clock3,
  Menu,
  Plus,
  Settings,
  X,
} from "lucide-react";
import {
  usePathname,
  useRouter,
  useSearchParams,
  type ReadonlyURLSearchParams,
} from "next/navigation";
import { useTranslation } from "react-i18next";
import { AdminLink } from "@/components/auth/AdminLink";
import { LogoutButton } from "@/components/auth/LogoutButton";
import {
  BRAND_LOGO_SRC,
  BRAND_NAME,
  PRIMARY_NAV,
} from "@/components/navigation/app-nav";
import { formatRelativeTime } from "@/lib/relative-time";
import { listSessions, type SessionSummary } from "@/lib/session-api";
import { surfaceForPath } from "@/lib/session-surfaces";

function pathMatches(pathname: string, prefix: string) {
  return pathname === prefix || pathname.startsWith(`${prefix}/`);
}

function shouldRenderChrome(pathname: string) {
  return !["/login", "/register", "/admin"].some((prefix) =>
    pathMatches(pathname, prefix),
  );
}

function activeSessionIdFromPath(pathname: string, basePath: string) {
  const prefix = `${basePath}/`;
  if (!pathname.startsWith(prefix)) return null;
  const candidate = pathname.slice(prefix.length).split("/")[0];
  return candidate || null;
}

type ChromeConfig =
  | { mode: "menu"; title: string; backHref?: never }
  | { mode: "back"; title: string; backHref?: string };

function resolveChromeConfig(
  pathname: string,
  searchParams: ReadonlyURLSearchParams,
  t: (key: string) => string,
): ChromeConfig {
  if (pathMatches(pathname, "/chat") || pathMatches(pathname, "/co-learn")) {
    return { mode: "menu", title: BRAND_NAME };
  }

  if (pathname === "/knowledge" && searchParams.get("kb")) {
    return { mode: "back", title: t("Knowledge"), backHref: "/knowledge" };
  }

  if (pathname.startsWith("/agents/") && pathname.endsWith("/chat")) {
    return { mode: "back", title: t("TutorBot"), backHref: "/agents" };
  }

  if (pathname.startsWith("/co-writer/")) {
    return { mode: "back", title: t("Co-Writer"), backHref: "/co-writer" };
  }

  if (pathMatches(pathname, "/settings")) {
    return { mode: "back", title: t("Settings") };
  }

  if (pathMatches(pathname, "/knowledge")) {
    return { mode: "back", title: t("Knowledge") };
  }

  if (pathMatches(pathname, "/space")) {
    return { mode: "back", title: t("Space") };
  }

  const matchedPrimary = PRIMARY_NAV.find((item) =>
    pathMatches(pathname, item.href),
  );
  if (matchedPrimary) {
    return { mode: "back", title: t(matchedPrimary.label) };
  }

  return { mode: "menu", title: BRAND_NAME };
}

export default function MobileAppChrome() {
  const pathname = usePathname() ?? "";
  const searchParams = useSearchParams();
  const router = useRouter();
  const { t, i18n } = useTranslation();
  const routeKey = `${pathname}?${searchParams.toString()}`;
  const surface = useMemo(() => surfaceForPath(pathname), [pathname]);
  const chromeConfig = useMemo(
    () => resolveChromeConfig(pathname, searchParams, t),
    [pathname, searchParams, t],
  );
  const [drawerOpenKey, setDrawerOpenKey] = useState<string | null>(null);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [recentSessions, setRecentSessions] = useState<SessionSummary[]>([]);
  const drawerOpen = drawerOpenKey === routeKey;

  const activeSessionId = useMemo(
    () => activeSessionIdFromPath(pathname, surface.basePath),
    [pathname, surface.basePath],
  );
  const chromeVisible = shouldRenderChrome(pathname);

  const closeDrawer = useCallback(() => {
    setDrawerOpenKey(null);
  }, []);

  const openDrawer = useCallback(() => {
    setLoadingSessions(true);
    setDrawerOpenKey(routeKey);
  }, [routeKey]);

  const handleNavigate = useCallback(
    (href: string) => {
      closeDrawer();
      router.push(href);
    },
    [closeDrawer, router],
  );

  const handleBack = useCallback(() => {
    if (chromeConfig.mode === "back" && chromeConfig.backHref) {
      router.push(chromeConfig.backHref);
      return;
    }
    if (typeof window !== "undefined" && window.history.length > 1) {
      router.back();
      return;
    }
    router.push(surface.basePath);
  }, [chromeConfig, router, surface.basePath]);

  const handleNewChat = useCallback(() => {
    router.push(surface.basePath);
  }, [router, surface.basePath]);

  useEffect(() => {
    if (!drawerOpen || chromeConfig.mode !== "menu") return;
    let cancelled = false;
    void listSessions(12, 0, { force: true, kind: surface.kind })
      .then((sessions) => {
        if (!cancelled) {
          setRecentSessions(sessions);
        }
      })
      .catch((error) => {
        console.error("Failed to load mobile recents", error);
        if (!cancelled) {
          setRecentSessions([]);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoadingSessions(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [chromeConfig.mode, drawerOpen, surface.kind]);

  useEffect(() => {
    if (!drawerOpen) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [drawerOpen]);

  if (!chromeVisible) return null;

  return (
    <>
      <header
        className="fixed inset-x-0 top-0 z-50 border-b border-[var(--border)]/40 bg-[var(--secondary)]/92 backdrop-blur-md md:hidden"
        style={{ paddingTop: "env(safe-area-inset-top)" }}
      >
        <div className="grid h-14 grid-cols-[40px_1fr_40px] items-center gap-2 px-3">
          {chromeConfig.mode === "menu" ? (
            <button
              type="button"
              onClick={openDrawer}
              aria-label={t("Open menu")}
              className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-black/10 text-[var(--foreground)] transition-colors hover:bg-black/20"
            >
              <Menu size={18} strokeWidth={2.1} />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleBack}
              aria-label={t("Back")}
              className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-black/10 text-[var(--foreground)] transition-colors hover:bg-black/20"
            >
              <ArrowLeft size={18} strokeWidth={2.1} />
            </button>
          )}

          <div className="min-w-0 justify-self-center">
            {chromeConfig.mode === "menu" ? (
              <div className="flex items-center gap-2">
                <Image
                  src={BRAND_LOGO_SRC}
                  alt={BRAND_NAME}
                  width={20}
                  height={20}
                  unoptimized
                  className="h-5 w-auto shrink-0"
                />
                <span className="truncate text-[14px] font-semibold tracking-[-0.02em] text-[var(--foreground)]">
                  {BRAND_NAME}
                </span>
              </div>
            ) : (
              <span className="block truncate text-[14px] font-semibold tracking-[-0.02em] text-[var(--foreground)]">
                {chromeConfig.title}
              </span>
            )}
          </div>

          <button
            type="button"
            onClick={handleNewChat}
            aria-label={t("New Chat")}
            className="flex h-10 w-10 items-center justify-center rounded-full border border-[var(--primary)]/35 bg-[var(--primary)] text-[var(--primary-foreground)] shadow-[0_10px_26px_rgba(201,162,39,0.18)] transition-opacity hover:opacity-90"
          >
            <Plus size={18} strokeWidth={2.2} />
          </button>
        </div>
      </header>

      {chromeConfig.mode === "menu" && (
        <>
          <button
            type="button"
            aria-label={t("Close menu")}
            onClick={closeDrawer}
            className={`fixed inset-0 z-40 bg-slate-950/60 transition-opacity md:hidden ${
              drawerOpen
                ? "pointer-events-auto opacity-100"
                : "pointer-events-none opacity-0"
            }`}
          />

          <aside
            className={`fixed left-0 top-0 z-50 flex h-[100dvh] w-[min(86vw,360px)] flex-col overflow-hidden bg-[#071b2d] text-white shadow-[0_24px_80px_rgba(0,0,0,0.45)] transition-transform duration-300 ease-out md:hidden ${
              drawerOpen ? "translate-x-0" : "-translate-x-full"
            }`}
            style={{ paddingTop: "env(safe-area-inset-top)" }}
          >
            <div className="flex items-center justify-between px-5 py-4">
              <div className="flex items-center gap-2.5">
                <Image
                  src={BRAND_LOGO_SRC}
                  alt={BRAND_NAME}
                  width={28}
                  height={28}
                  unoptimized
                  className="h-7 w-auto shrink-0"
                />
                <div>
                  <p className="text-[16px] font-semibold tracking-[-0.02em] text-white">
                    {BRAND_NAME}
                  </p>
                  <p className="text-[11px] text-slate-400">
                    {t("Intelligent learning workspace")}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={closeDrawer}
                aria-label={t("Close menu")}
                className="flex h-9 w-9 items-center justify-center rounded-full border border-white/10 bg-white/5 text-slate-200 transition-colors hover:bg-white/10"
              >
                <X size={16} strokeWidth={2.1} />
              </button>
            </div>

            <div className="px-3 pb-3">
              <nav className="space-y-1">
                {PRIMARY_NAV.map((item) => {
                  const active = pathMatches(pathname, item.href);
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.href}
                      type="button"
                      onClick={() => handleNavigate(item.href)}
                      className={`flex w-full items-center gap-3 rounded-2xl px-3.5 py-3 text-left text-[14px] transition-colors ${
                        active
                          ? "bg-white/12 text-white ring-1 ring-white/10"
                          : "text-slate-300 hover:bg-white/6 hover:text-white"
                      }`}
                    >
                      <Icon size={17} strokeWidth={active ? 2.1 : 1.8} />
                      <span className="font-medium">{t(item.label)}</span>
                    </button>
                  );
                })}
              </nav>
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto border-t border-white/8 px-4 py-4">
              <div className="mb-3 flex items-center gap-2 text-[12px] font-semibold uppercase tracking-[0.18em] text-slate-400">
                <Clock3 size={13} strokeWidth={1.8} />
                <span>{t("Recents")}</span>
              </div>

              {loadingSessions ? (
                <div className="space-y-2">
                  {[1, 2, 3, 4].map((item) => (
                    <div
                      key={item}
                      className="h-14 animate-pulse rounded-2xl bg-white/6"
                    />
                  ))}
                </div>
              ) : recentSessions.length > 0 ? (
                <div className="space-y-1.5">
                  {recentSessions.map((session) => {
                    const active = session.session_id === activeSessionId;
                    return (
                      <button
                        key={session.session_id}
                        type="button"
                        onClick={() =>
                          handleNavigate(
                            `${surface.basePath}/${session.session_id}`,
                          )
                        }
                        className={`flex w-full flex-col rounded-2xl px-3.5 py-3 text-left transition-colors ${
                          active
                            ? "bg-white/12 ring-1 ring-white/10"
                            : "hover:bg-white/6"
                        }`}
                      >
                        <span className="truncate text-[13.5px] font-medium text-white">
                          {session.title || t("Untitled chat")}
                        </span>
                        <span className="mt-1 truncate text-[11px] text-slate-400">
                          {formatRelativeTime(
                            session.updated_at,
                            i18n.language,
                          )}
                        </span>
                      </button>
                    );
                  })}
                </div>
              ) : (
                <div className="rounded-2xl border border-dashed border-white/10 px-4 py-6 text-center text-[12px] text-slate-400">
                  {t("No conversations yet")}
                </div>
              )}
            </div>

            <div className="border-t border-white/8 px-4 py-4">
              <button
                type="button"
                onClick={() => handleNavigate("/settings")}
                className="mb-2 flex w-full items-center gap-3 rounded-2xl px-3.5 py-3 text-left text-[14px] text-slate-300 transition-colors hover:bg-white/6 hover:text-white"
              >
                <Settings size={17} strokeWidth={1.8} />
                <span className="font-medium">{t("Settings")}</span>
              </button>

              <div className="[&_a]:text-slate-300 [&_a:hover]:bg-white/6 [&_a:hover]:text-white [&_button]:text-slate-300 [&_button:hover]:bg-white/6 [&_button:hover]:text-white">
                <AdminLink />
                <LogoutButton />
              </div>
            </div>
          </aside>
        </>
      )}
    </>
  );
}
