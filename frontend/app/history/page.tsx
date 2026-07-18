"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { format } from "date-fns";
import { Trash2, ArrowRight } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";
import { api } from "@/services/api";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { CircularScore } from "@/components/ui/circular-score";
import { useAuth } from "@/context/AuthContext";
import { DeleteConfirmDialog } from "@/components/ui/delete-confirm-dialog";

export default function HistoryPage() {
  const queryClient = useQueryClient();
  const { user } = useAuth();

  // Track which record is awaiting deletion — null means the dialog is closed.
  const [pendingDeleteId, setPendingDeleteId] = useState<string | null>(null);

  const { data: history, isLoading, isError, refetch } = useQuery({
    queryKey: ["history", user?.id || "guest"],
    queryFn: () => api.getHistory(user?.id || "guest"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.deleteHistory(id),
    onSuccess: () => {
      toast.success("Analysis deleted.");
      queryClient.invalidateQueries({ queryKey: ["history"] });
      setPendingDeleteId(null);
    },
    onError: () => {
      toast.error("Failed to delete analysis.");
      setPendingDeleteId(null);
    },
  });

  const handleDeleteRequest = (id: string) => setPendingDeleteId(id);
  const handleDeleteCancel = () => setPendingDeleteId(null);
  const handleDeleteConfirm = () => {
    if (pendingDeleteId) deleteMutation.mutate(pendingDeleteId);
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold tracking-tight">History</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-[250px] rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold tracking-tight">History</h1>
        <ErrorState message="Could not load your history." retryAction={() => refetch()} />
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Analysis History</h1>
        </div>

        {!history || history.length === 0 ? (
          <EmptyState 
            title="No history found" 
            description="You haven't run any CV analyses yet. Head to the Dashboard to get started." 
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {history.map((item) => (
              <Card key={item.id} className="glass-card flex flex-col hover:border-primary/50 transition-colors group">
                <CardHeader className="pb-4">
                  <div className="flex justify-between items-start">
                    <div className="text-xs text-muted-foreground">
                      {format(new Date(item.created_at), "MMM d, yyyy • h:mm a")}
                    </div>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-8 w-8 text-muted-foreground hover:text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                      onClick={() => handleDeleteRequest(item.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col items-center gap-4">
                  <CircularScore score={item.match_score} size={80} strokeWidth={6} />
                  <p className="text-sm text-center text-muted-foreground line-clamp-3">
                    {item.summary}
                  </p>
                </CardContent>
                <CardFooter className="pt-0">
                  <Link href={`/analysis/${item.id}`} className="w-full">
                    <Button variant="secondary" className="w-full">
                      View Details
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>

      <DeleteConfirmDialog
        open={pendingDeleteId !== null}
        onCancel={handleDeleteCancel}
        onConfirm={handleDeleteConfirm}
        isPending={deleteMutation.isPending}
      />
    </>
  );
}
