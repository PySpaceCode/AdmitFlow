import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Allow normal routing, no more forced root redirects
  return NextResponse.next();
}

export const config = {
  matcher: [],
};
