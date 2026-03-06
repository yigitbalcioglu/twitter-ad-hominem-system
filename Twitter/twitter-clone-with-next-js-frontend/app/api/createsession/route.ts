// pages/api/create-session.ts

import { NextRequest } from 'next/server';
import { createSession } from '@/lib/session';

export async function POST(req: NextRequest) {

    const { userId } = await req.json();
    try {
        await createSession(userId);
        return Response.json({ message: "Success" }, { status: 201 })
    } catch (error) {

        return Response.json({ message: "Internal Error" }, { status: 500 })
    }
}
