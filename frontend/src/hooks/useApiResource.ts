import { useCallback, useEffect, useState } from "react";
import { describeError } from "../utils/errors";

export interface ApiResource<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refresh: () => void;
}

export function useApiResource<T>(load: () => Promise<T>): ApiResource<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshCount, setRefreshCount] = useState(0);

  useEffect(() => {
    let isCurrent = true;
    setLoading(true);
    setError(null);
    load()
      .then((result) => {
        if (isCurrent) setData(result);
      })
      .catch((reason: unknown) => {
        if (isCurrent) setError(describeError(reason));
      })
      .finally(() => {
        if (isCurrent) setLoading(false);
      });
    return () => {
      isCurrent = false;
    };
  }, [load, refreshCount]);

  const refresh = useCallback(() => setRefreshCount((count) => count + 1), []);

  return { data, loading, error, refresh };
}
