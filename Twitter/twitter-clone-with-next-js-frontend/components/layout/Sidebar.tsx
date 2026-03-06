"use client"
import { CiTwitter } from "react-icons/ci";
import { CgProfile } from "react-icons/cg";
import { FaHome } from "react-icons/fa";
import { FiLogIn, FiUserPlus } from "react-icons/fi";
import { HiOutlineChatBubbleLeftRight } from "react-icons/hi2";
import Sidebarlogo from "./Sidebarlogo";
import { SidebarItem } from "./SidebarItem";

export default function Sidebar() {
    const items = [
        {
            label: "Home",
            href: "/home",
            icon: FaHome,
        },
        {
            label: "Profile",
            href: "/profile",
            icon: CgProfile,
        },
        {
            label: "Messages",
            href: "/messages",
            icon: HiOutlineChatBubbleLeftRight,
        },
        {
            label: "Login",
            href: "/login",
            icon: FiLogIn,
        },
        {
            label: "Sign up",
            href: "/register",
            icon: FiUserPlus,
        },
    ];

    return (
        <div className="fixed inset-x-0 bottom-0 z-40 border-t border-neutral-800 bg-black/95 px-2 py-2 backdrop-blur lg:static lg:h-full lg:border-t-0 lg:bg-transparent lg:px-0 lg:py-0 lg:backdrop-blur-none">
            <div className="mx-auto flex max-w-md items-center justify-center lg:h-full lg:max-w-none lg:justify-end xl:justify-start">
                <div className="flex w-full items-center justify-between lg:w-[230px] lg:flex-col lg:items-stretch lg:justify-start lg:space-y-2">
                    <Sidebarlogo />
                    {items.map((item) => (
                        <SidebarItem
                            key={item.href}
                            href={item.href}
                            label={item.label}
                            icon={item.icon}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}