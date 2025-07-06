import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function formatCategoryName(categoryName: string): string {
  return categoryName
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
