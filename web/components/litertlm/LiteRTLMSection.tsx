"use client";

import { Cpu, HardDrive } from "lucide-react";
import { useTranslation } from "react-i18next";
import HardwareSpecsCard from "./HardwareSpecsCard";
import ModelCatalog from "./ModelCatalog";
import DownloadedModels from "./DownloadedModels";

export default function LiteRTLMSection() {
  const { t } = useTranslation();

  return (
    <div className="space-y-8">
      {/* Hardware Specs */}
      <section>
        <div className="mb-4 flex items-center gap-2">
          <Cpu className="h-5 w-5 text-[var(--muted-foreground)]" />
          <h2 className="text-lg font-semibold text-[var(--foreground)]">
            Hardware Specifications
          </h2>
        </div>
        <HardwareSpecsCard />
      </section>

      {/* Model Catalog */}
      <section>
        <div className="mb-4 flex items-center gap-2">
          <HardDrive className="h-5 w-5 text-[var(--muted-foreground)]" />
          <h2 className="text-lg font-semibold text-[var(--foreground)]">
            Available Models
          </h2>
        </div>
        <ModelCatalog />
      </section>

      {/* Downloaded Models */}
      <section>
        <div className="mb-4 flex items-center gap-2">
          <HardDrive className="h-5 w-5 text-[var(--muted-foreground)]" />
          <h2 className="text-lg font-semibold text-[var(--foreground)]">
            Downloaded Models
          </h2>
        </div>
        <DownloadedModels />
      </section>
    </div>
  );
}
