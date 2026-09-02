import type { Business } from "../types";

interface HeaderProps {
  email: string;
  businesses: Business[];
  selectedBusiness: Business;
  onSelectBusiness: (businessId: string) => void;
}

export function Header({ email, businesses, selectedBusiness, onSelectBusiness }: HeaderProps) {
  return (
    <header className="app-header">
      <div>
        <span className="app-name">Ledgerly</span>
        <h1 className="business-name">{selectedBusiness.name}</h1>
      </div>
      <div className="header-account">
        {businesses.length > 1 && (
          <label>
            <span className="visually-hidden">Business</span>
            <select
              value={selectedBusiness.business_id}
              onChange={(event) => onSelectBusiness(event.target.value)}
            >
              {businesses.map((business) => (
                <option key={business.business_id} value={business.business_id}>
                  {business.name}
                </option>
              ))}
            </select>
          </label>
        )}
        <span>{email}</span>
      </div>
    </header>
  );
}
