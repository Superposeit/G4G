import type { Metadata } from "next";
import { Plus_Jakarta_Sans, Lora, Space_Grotesk } from "next/font/google";
import "./globals.css";
import ThemeScript from "@/components/ThemeScript";
import ToastViewport from "@/components/common/ToastViewport";
import { AppShellProvider } from "@/context/AppShellContext";
import { I18nClientBridge } from "@/i18n/I18nClientBridge";

const fontSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-sans",
});

const fontSerif = Lora({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-serif",
});

const fontDisplay = Space_Grotesk({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-display",
});

export const metadata: Metadata = {
  title: "EducaT TutorRD",
  description: "Agent-native tutoring and intelligent learning companion",
  icons: {
    icon: [
      {
        url: "/educat-tutorrd-favicon-16x16-v3.png",
        sizes: "16x16",
        type: "image/png",
      },
      {
        url: "/educat-tutorrd-favicon-32x32-v3.png",
        sizes: "32x32",
        type: "image/png",
      },
    ],
    shortcut: "/educat-tutorrd-favicon-32x32-v3.png",
    apple: "/educat-tutorrd-apple-touch-icon-v3.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      data-scroll-behavior="smooth"
      className={`${fontSans.variable} ${fontSerif.variable} ${fontDisplay.variable}`}
    >
      <head>
        <ThemeScript />
      </head>
      <body className="font-sans bg-[var(--background)] text-[var(--foreground)]">
        <AppShellProvider>
          <I18nClientBridge>{children}</I18nClientBridge>
          <ToastViewport />
        </AppShellProvider>
      </body>
    </html>
  );
}
