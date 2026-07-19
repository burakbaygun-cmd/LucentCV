"use client";

import { Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

// ─── Types ───────────────────────────────────────────────────────────────────

interface DeleteConfirmDialogProps {
  /** Controls whether the dialog is visible. */
  open: boolean;
  /** Called when the user dismisses the dialog without confirming. */
  onCancel: () => void;
  /** Called when the user explicitly confirms the destructive action. */
  onConfirm: () => void;
  /** When true, the confirm button enters a loading state to reflect async work in progress. */
  isPending?: boolean;
  /** Optional override for the dialog title. */
  title?: string;
  /** Optional override for the supporting description text. */
  description?: string;
}

// ─── Component ───────────────────────────────────────────────────────────────

/**
 * DeleteConfirmDialog
 *
 * A reusable, accessible confirmation dialog for destructive actions.
 * Built on top of the project's @base-ui Dialog primitives to stay consistent
 * with the existing design system — no external Radix dependency needed.
 *
 * Usage:
 *   <DeleteConfirmDialog
 *     open={isOpen}
 *     onCancel={() => setIsOpen(false)}
 *     onConfirm={handleDelete}
 *     isPending={deleteMutation.isPending}
 *   />
 */
export function DeleteConfirmDialog({
  open,
  onCancel,
  onConfirm,
  isPending = false,
  title = "Delete this record?",
  description = "This action is permanent and cannot be undone. The analysis record will be removed from your history.",
}: DeleteConfirmDialogProps) {
  return (
    // Suppress the close button — the user must make an explicit choice.
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onCancel()}>
      <DialogContent showCloseButton={false} className="max-w-sm">
        <DialogHeader>
          {/* Dialog heading — kept concise and action-oriented. */}
          <DialogTitle>{title}</DialogTitle>

          {/* Supporting copy that explains the consequence of the action. */}
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>

        <DialogFooter>
          {/* Safe exit — lets users change their mind without side effects. */}
          <Button variant="outline" onClick={onCancel} disabled={isPending}>
            Cancel
          </Button>

          {/* Confirm destructive action — visually distinct to prevent accidental clicks. */}
          <Button variant="destructive" onClick={onConfirm} disabled={isPending}>
            {isPending ? (
              // Provide inline feedback while the async delete is in flight.
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Deleting…
              </>
            ) : (
              "Delete"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
