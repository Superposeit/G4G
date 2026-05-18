"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { type ReactNode } from "react";
import { useAppShell } from "@/context/AppShellContext";
import {
  Github,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  BRAND_LOGO_SRC,
  BRAND_NAME,
  GITHUB_REPO_URL,
  PRIMARY_NAV,
  SECONDARY_NAV,
} from "@/components/navigation/app-nav";
import SessionList from "@/components/SessionList";
import { surfaceForPath } from "@/lib/session-surfaces";
import { TutorBotRecent } from "@/components/sidebar/TutorBotRecent";
import { VersionBadge } from "@/components/sidebar/VersionBadge";
import type { SessionSummary } from "@/lib/session-api";
import { Tooltip } from "@/components/ui/Tooltip";
const DEFAULT_SESSION_VIEWPORT_CLASS_NAME = "max-h-[112px]";

interface SidebarShellProps {
  sessions?: SessionSummary[];
  activeSessionId?: string | null;
  loadingSessions?: boolean;
  showSessions?: boolean;
  sessionViewportClassName?: string;
  onNewChat?: () => void;
  onSelectSession?: (sessionId: string) => void | Promise<void>;
  onRenameSession?: (sessionId: string, title: string) => void | Promise<void>;
  onDeleteSession?: (sessionId: string) => void | Promise<void>;
  footerSlot?: ReactNode;
}

export function SidebarShell({
  sessions = [],
  activeSessionId = null,
  loadingSessions = false,
  showSessions = false,
  sessionViewportClassName = DEFAULT_SESSION_VIEWPORT_CLASS_NAME,
  onNewChat,
  onSelectSession,
  onRenameSession,
  onDeleteSession,
  footerSlot,
}: SidebarShellProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useTranslation();
  const {
    sidebarCollapsed: collapsed,
    setSidebarCollapsed: setCollapsed,
    mobileSidebarOpen,
    setMobileSidebarOpen,
  } = useAppShell();

  const handleNewChat = () => {
    if (onNewChat) {
      onNewChat();
    } else {
      router.push("/chat");
    }
    setMobileSidebarOpen(false);
  };

  const handleNavClick = () => {
    setMobileSidebarOpen(false);
  };

  /* ---- Collapsed state ---- */
  if (collapsed) {
    return (
      <aside className="group/sb relative flex h-screen w-[64px] shrink-0 flex-col items-center border-r border-[var(--border)]/55 bg-[var(--secondary)]/95 py-3 backdrop-blur-sm transition-all duration-200">
        {/* Header: logo + collapse toggle (toggle replaces logo on hover) */}
        <div className="relative mb-2 flex h-9 w-9 items-center justify-center">
          <Link
            href="/"
            aria-label={BRAND_NAME}
            className="flex items-center justify-center transition-opacity duration-150 group-hover/sb:opacity-0"
          >
            <Image
              src={BRAND_LOGO_SRC}
              alt={BRAND_NAME}
              width={26}
              height={26}
              unoptimized
              className="h-[26px] w-auto"
            />
          </Link>
          <button
            onClick={() => setCollapsed(false)}
            className="absolute inset-0 flex items-center justify-center rounded-lg text-[var(--muted-foreground)] opacity-0 transition-all duration-150 hover:bg-[var(--primary)]/14 hover:text-[var(--foreground)] group-hover/sb:opacity-100"
            aria-label={t("Expand sidebar")}
          >
            <PanelLeftOpen size={16} />
          </button>
        </div>

        {/* New chat — visually distinct circular button */}
        <button
          onClick={handleNewChat}
          title={t("New Chat") as string}
          className="mb-2 flex h-9 w-9 items-center justify-center rounded-xl border border-[var(--primary)]/45 bg-[var(--primary)] text-[var(--primary-foreground)] shadow-[0_10px_28px_rgba(201,162,39,0.2)] transition-all duration-150 hover:brightness-105"
          aria-label={t("New Chat")}
        >
          <Plus size={16} strokeWidth={2.2} />
        </button>

        <div className="my-1.5 h-px w-7 bg-[var(--border)]/40" />

        {/* Primary nav */}
        <nav className="flex w-full flex-col items-center gap-1 px-1.5">
          {PRIMARY_NAV.map((item) => {
            const active = pathname.startsWith(item.href);
            const description = item.tooltipKey
              ? t(item.tooltipKey)
              : undefined;
            return (
              <Tooltip
                key={item.href}
                label={t(item.label)}
                description={description}
                side="right"
              >
                <Link
                  href={item.href}
                  aria-label={t(item.label)}
                  className={`relative flex h-9 w-9 items-center justify-center rounded-xl transition-all duration-150 ${
                    active
                      ? "bg-[var(--primary)]/16 text-[var(--foreground)] shadow-sm ring-1 ring-[var(--primary)]/18"
                      : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/45 hover:text-[var(--foreground)]"
                  }`}
                >
                  {active && (
                    <span className="absolute -left-1.5 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full bg-[var(--primary)]" />
                  )}
                  <item.icon size={18} strokeWidth={active ? 2 : 1.6} />
                </Link>
              </Tooltip>
            );
          })}
        </nav>

        <div className="flex-1" />

        {/* Secondary nav + footer */}
        <div className="flex w-full flex-col items-center gap-1 px-1.5">
          <div className="my-1 h-px w-7 bg-[var(--border)]/40" />
          {SECONDARY_NAV.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                title={t(item.label) as string}
                className={`relative flex h-9 w-9 items-center justify-center rounded-xl transition-all duration-150 ${
                  active
                    ? "bg-[var(--primary)]/16 text-[var(--foreground)] shadow-sm ring-1 ring-[var(--primary)]/18"
                    : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/45 hover:text-[var(--foreground)]"
                }`}
              >
                {active && (
                  <span className="absolute -left-1.5 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full bg-[var(--primary)]" />
                )}
                <item.icon size={18} strokeWidth={active ? 2 : 1.6} />
              </Link>
            );
          })}
          {footerSlot}
          <a
            href={GITHUB_REPO_URL}
            target="_blank"
            rel="noreferrer noopener"
            title={t("GitHub") as string}
            aria-label={t("GitHub")}
            className="mt-1 flex h-9 w-9 items-center justify-center rounded-xl text-[var(--muted-foreground)]/70 transition-colors hover:bg-[var(--primary)]/14 hover:text-[var(--foreground)]"
          >
            <Github size={15} strokeWidth={1.6} />
          </a>
          <VersionBadge collapsed />
        </div>
      </aside>
    );
  }

  /* ---- Expanded state ---- */
  return (
    <>
      {/* Desktop sidebar — hidden on mobile */}
      <div className="hidden md:contents">
        <aside className="flex h-screen w-[220px] shrink-0 flex-col border-r border-[var(--border)]/55 bg-[var(--secondary)]/95 backdrop-blur-sm transition-all duration-200">
          {/* Header: logo + collapse toggle */}
          <div className="flex h-14 items-center justify-between px-4">
            <Link href="/" className="group flex items-center gap-2" onClick={handleNavClick}>
              <Image
                src={BRAND_LOGO_SRC}
                alt={BRAND_NAME}
                width={28}
                height={28}
                unoptimized
                className="h-7 w-auto transition-transform duration-200 group-hover:scale-105"
              />
              <span className="text-[16px] font-semibold leading-none tracking-[-0.02em] text-[var(--foreground)]">
                {BRAND_NAME}
              </span>
            </Link>
            <button
              onClick={() => setCollapsed(true)}
              className="rounded-md p-1 text-[var(--muted-foreground)] transition-colors hover:bg-[var(--primary)]/12 hover:text-[var(--foreground)]"
              aria-label={t("Collapse sidebar")}
            >
              <PanelLeftClose size={15} />
            </button>
          </div>

          <nav className="px-2 pt-1">
            <div className="space-y-px">
              <button
                onClick={handleNewChat}
                className="flex w-full items-center gap-2.5 rounded-lg border border-[var(--primary)]/32 bg-[var(--primary)] px-3 py-2 text-[13.5px] font-medium text-[var(--primary-foreground)] shadow-[0_12px_30px_rgba(201,162,39,0.16)] transition-all hover:brightness-105"
              >
                <Plus size={16} strokeWidth={2} />
                <span>{t("New Chat")}</span>
              </button>

              {PRIMARY_NAV.map((item) => {
                const active = pathname.startsWith(item.href);
                // Sessions hang under whichever surface entry owns the current
                // URL. Single source of truth: ``lib/session-surfaces``.
                const sessionsOwnerHref = surfaceForPath(pathname).basePath;
                const hasSessionsBelow =
                  item.href === sessionsOwnerHref &&
                  showSessions &&
                  onSelectSession &&
                  onRenameSession &&
                  onDeleteSession;
                const hasBots = item.href === "/agents";
                return (
                  <div key={item.href}>
                    <Link
                      href={item.href}
                      onClick={handleNavClick}
                      className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13.5px] transition-colors ${
                        active
                          ? "bg-[var(--primary)]/14 font-medium text-[var(--foreground)] ring-1 ring-[var(--primary)]/15"
                          : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/45 hover:text-[var(--foreground)]"
                      }`}
                    >
                      <item.icon size={16} strokeWidth={active ? 1.9 : 1.5} />
                      <span>{t(item.label)}</span>
                    </Link>
                    {hasSessionsBelow && (
                      <div
                        className={`${sessionViewportClassName} overflow-y-auto`}
                      >
                        <SessionList
                          sessions={sessions}
                          activeSessionId={activeSessionId}
                          loading={loadingSessions}
                          onSelect={onSelectSession}
                          onRename={onRenameSession}
                          onDelete={onDeleteSession}
                          compact
                        />
                      </div>
                    )}
                    {hasBots && <TutorBotRecent />}
                  </div>
                );
              })}
            </div>
          </nav>

          <div className="flex-1" />

          <div className="border-t border-[var(--border)]/40 px-2 py-2">
            {SECONDARY_NAV.map((item) => {
              const active = pathname.startsWith(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={handleNavClick}
                  className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13.5px] transition-colors ${
                    active
                      ? "bg-[var(--primary)]/14 font-medium text-[var(--foreground)] ring-1 ring-[var(--primary)]/15"
                      : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/45 hover:text-[var(--foreground)]"
                  }`}
                >
                  <item.icon size={16} strokeWidth={active ? 1.9 : 1.5} />
                  <span>{t(item.label)}</span>
                </Link>
              );
            })}
            {footerSlot}
            <div className="mt-0.5 flex items-center gap-0.5">
              <VersionBadge />
              <a
                href={GITHUB_REPO_URL}
                target="_blank"
                rel="noreferrer noopener"
                title={t("GitHub") as string}
                aria-label={t("GitHub")}
                className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-[var(--muted-foreground)]/55 transition-colors hover:bg-[var(--primary)]/12 hover:text-[var(--foreground)]"
              >
                <Github size={13} strokeWidth={1.7} />
              </a>
            </div>
          </div>
        </aside>
      </div>

      {/* Mobile drawer */}
      {mobileSidebarOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40 bg-black/50 md:hidden"
            onClick={() => setMobileSidebarOpen(false)}
            aria-hidden="true"
          />
          {/* Drawer — always expanded on mobile */}
          <div className="fixed inset-y-0 left-0 z-50 md:hidden">
            <aside className="flex h-screen w-[220px] shrink-0 flex-col border-r border-[var(--border)]/55 bg-[var(--secondary)]/95 backdrop-blur-sm transition-all duration-200">
              {/* Header: logo + collapse toggle */}
              <div className="flex h-14 items-center justify-between px-4">
                <Link href="/" className="group flex items-center gap-2" onClick={handleNavClick}>
                  <Image
                    src={BRAND_LOGO_SRC}
                    alt={BRAND_NAME}
                    width={28}
                    height={28}
                    unoptimized
                    className="h-7 w-auto transition-transform duration-200 group-hover:scale-105"
                  />
                  <span className="text-[16px] font-semibold leading-none tracking-[-0.02em] text-[var(--foreground)]">
                    {BRAND_NAME}
                  </span>
                </Link>
                <button
                  onClick={() => setMobileSidebarOpen(false)}
                  className="rounded-md p-1 text-[var(--muted-foreground)] transition-colors hover:bg-[var(--primary)]/12 hover:text-[var(--foreground)]"
                  aria-label={t("Close sidebar")}
                >
                  <PanelLeftClose size={15} />
                </button>
              </div>

              <nav className="px-2 pt-1">
                <div className="space-y-px">
                  <button
                    onClick={handleNewChat}
                    className="flex w-full items-center gap-2.5 rounded-lg border border-[var(--primary)]/32 bg-[var(--primary)] px-3 py-2 text-[13.5px] font-medium text-[var(--primary-foreground)] shadow-[0_12px_30px_rgba(201,162,39,0.16)] transition-all hover:brightness-105"
                  >
                    <Plus size={16} strokeWidth={2} />
                    <span>{t("New Chat")}</span>
                  </button>

                  {PRIMARY_NAV.map((item) => {
                    const active = pathname.startsWith(item.href);
                    const sessionsOwnerHref = surfaceForPath(pathname).basePath;
                    const hasSessionsBelow =
                      item.href === sessionsOwnerHref &&
                      showSessions &&
                      onSelectSession &&
                      onRenameSession &&
                      onDeleteSession;
                    const hasBots = item.href === "/agents";
                    return (
                      <div key={item.href}>
                        <Link
                          href={item.href}
                          onClick={handleNavClick}
                          className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13.5px] transition-colors ${
                            active
                              ? "bg-[var(--primary)]/14 font-medium text-[var(--foreground)] ring-1 ring-[var(--primary)]/15"
                              : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/45 hover:text-[var(--foreground)]"
                          }`}
                        >
                          <item.icon size={16} strokeWidth={active ? 1.9 : 1.5} />
                          <span>{t(item.label)}</span>
                        </Link>
                        {hasSessionsBelow && (
                          <div className={`${sessionViewportClassName} overflow-y-auto`}>
                            <SessionList
                              sessions={sessions}
                              activeSessionId={activeSessionId}
                              loading={loadingSessions}
                              onSelect={onSelectSession}
                              onRename={onRenameSession}
                              onDelete={onDeleteSession}
                              compact
                            />
                          </div>
                        )}
                        {hasBots && <TutorBotRecent />}
                      </div>
                    );
                  })}
                </div>
              </nav>

              <div className="flex-1" />

              <div className="border-t border-[var(--border)]/40 px-2 py-2">
                {SECONDARY_NAV.map((item) => {
                  const active = pathname.startsWith(item.href);
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={handleNavClick}
                      className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13.5px] transition-colors ${
                        active
                          ? "bg-[var(--primary)]/14 font-medium text-[var(--foreground)] ring-1 ring-[var(--primary)]/15"
                          : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/45 hover:text-[var(--foreground)]"
                      }`}
                    >
                      <item.icon size={16} strokeWidth={active ? 1.9 : 1.5} />
                      <span>{t(item.label)}</span>
                    </Link>
                  );
                })}
                {footerSlot}
                <div className="mt-0.5 flex items-center gap-0.5">
                  <VersionBadge />
                  <a
                    href={GITHUB_REPO_URL}
                    target="_blank"
                    rel="noreferrer noopener"
                    title={t("GitHub") as string}
                    aria-label={t("GitHub")}
                    className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-[var(--muted-foreground)]/55 transition-colors hover:bg-[var(--primary)]/12 hover:text-[var(--foreground)]"
                  >
                    <Github size={13} strokeWidth={1.7} />
                  </a>
                </div>
              </div>
            </aside>
          </div>
        </>
      )}
    </>
  );
}
