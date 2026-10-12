"""Tier 3: real browser against a live server and a real test database."""

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_user_creates_car_in_browser(page: Page, live_server) -> None:
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Corolla")
    page.get_by_label("Year", exact=True).fill("2024")
    page.get_by_label("Color", exact=False).fill("Silver")
    page.get_by_role("button", name="Create car", exact=True).click()

    expect(page.get_by_role("heading", name="Toyota Corolla", exact=True)).to_be_visible()
    expect(page.locator("#car-year")).to_have_text("2024")
    expect(page.locator("#car-model")).to_have_text("Corolla")


def test_user_edits_car_and_change_survives_reload(page: Page, live_server) -> None:
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Corolla")
    page.get_by_label("Year", exact=True).fill("2024")
    page.get_by_role("button", name="Create car", exact=True).click()
    expect(page.get_by_role("heading", name="Toyota Corolla", exact=True)).to_be_visible()

    page.get_by_role("link", name="Edit car", exact=True).click()
    expect(page.get_by_label("Model", exact=True)).to_have_value("Corolla")
    page.get_by_label("Model", exact=True).fill("Camry")
    page.get_by_label("Year", exact=True).fill("2025")
    page.get_by_role("button", name="Save changes", exact=True).click()
    expect(page.get_by_role("heading", name="Toyota Camry", exact=True)).to_be_visible()

    page.reload()
    expect(page.get_by_role("heading", name="Toyota Camry", exact=True)).to_be_visible()
    expect(page.locator("#car-model")).to_have_text("Camry")
    expect(page.locator("#car-year")).to_have_text("2025")
