import { AlertTriangle } from "lucide-react";
import { Button } from "./button";

interface ErrorStateProps {
  title?: string;
  message: string;
  retryAction?: () => void;
}

export function ErrorState({ title = "Something went wrong", message, retryAction }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center rounded-xl border border-destructive/20 bg-destructive/5 text-destructive">
      <AlertTriangle className="h-12 w-12 mb-4 opacity-80" />
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-sm opacity-80 mb-6 max-w-md">{message}</p>
      {retryAction && (
        <Button variant="destructive" onClick={retryAction}>
          Try Again
        </Button>
      )}
    </div>
  );
}
