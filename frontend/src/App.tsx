import { useState } from "react";
import { ErrorMessage } from "./components/ErrorMessage";
import { Header } from "./components/Header";
import { InvoicesTab } from "./components/InvoicesTab";
import { PaymentsTab } from "./components/PaymentsTab";
import { useMe } from "./hooks/useMe";

type TabId = "payments" | "invoices";

const TABS: ReadonlyArray<{ id: TabId; label: string }> = [
  { id: "payments", label: "Payments" },
  { id: "invoices", label: "Invoices" },
];

export function App() {
  const me = useMe();
  const [selectedBusinessId, setSelectedBusinessId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabId>("payments");

  if (me.error) {
    return (
      <main className="app-shell">
        <ErrorMessage message={me.error} />
        <button type="button" className="button" onClick={me.refresh} disabled={me.loading}>
          Try again
        </button>
      </main>
    );
  }

  if (!me.data) {
    return (
      <main className="app-shell">
        <p className="muted">Loading</p>
      </main>
    );
  }

  const { email, businesses } = me.data;
  if (businesses.length === 0) {
    return (
      <main className="app-shell">
        <p className="muted">{email} does not have access to any businesses yet.</p>
      </main>
    );
  }

  const selectedBusiness =
    businesses.find((business) => business.business_id === selectedBusinessId) ?? businesses[0];

  return (
    <div className="app-shell">
      <Header
        email={email}
        businesses={businesses}
        selectedBusiness={selectedBusiness}
        onSelectBusiness={setSelectedBusinessId}
      />
      <nav className="tabs" role="tablist" aria-label="Sections">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            type="button"
            role="tab"
            className="tab"
            aria-selected={tab.id === activeTab}
            aria-controls={`panel-${tab.id}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>
      <main id={`panel-${activeTab}`} role="tabpanel" aria-labelledby={`tab-${activeTab}`}>
        {activeTab === "payments" ? (
          <PaymentsTab key={selectedBusiness.business_id} businessId={selectedBusiness.business_id} />
        ) : (
          <InvoicesTab key={selectedBusiness.business_id} businessId={selectedBusiness.business_id} />
        )}
      </main>
    </div>
  );
}
