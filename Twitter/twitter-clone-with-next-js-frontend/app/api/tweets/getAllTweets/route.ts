import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers'
import { decrypt } from '@/lib/session';

export async function GET(req: NextRequest) {

    const cookie = cookies().get('session')?.value as string
    const session = await decrypt(cookie)

    try {
        const response = await fetch(`http://localhost:1337/api/posts?sort=createdAt:desc&filters[parent][$null]=true`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        const data = await response.json();
        return NextResponse.json(data);

    }
    catch (error) {
        return Response.json({ message: "Internal Error" }, { status: 500 })
    }
}