import calendar

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PRICE_PER_KWH = 0.2858  # in euro


def get_data() -> pd.DataFrame:
    """Create initial dataset."""
    data = {
        "month_name": [calendar.month_abbr[i + 1] for i in range(12)],
        "month_number": [i + 1 for i in range(12)],
        "energy_produced": [
            30.86,
            30.02,
            60.77,
            71.76,
            116.68,
            124.787,
            108.35,
            91.74,
            103.62,
            52.67,
            24.13,
            13,
        ],
        "energy_fed_into_grid": [
            6.06,
            4.49,
            19.38,
            20.79,
            41.14,
            37.71,
            32.43,
            21.00,
            32.57,
            16.99,
            3.61,
            2.31,
        ],
    }

    df = pd.DataFrame(data)
    df["energy_consumed"] = df["energy_produced"] - df["energy_fed_into_grid"]
    df["energy_consumed_relative"] = df["energy_consumed"] / df["energy_produced"] * 100

    return df


def plot_radar(df: pd.DataFrame) -> None:
    """Plot radar chart of energy production and consumption."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=df["energy_produced"],
            theta=df["month_name"],
            fill="toself",
            name="Solar Energy Produced [kWh]",
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=df["energy_fed_into_grid"],
            theta=df["month_name"],
            fill="toself",
            name="Solar Energy Fed Into Grid [kWh]",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        polar_angularaxis_rotation=90,
        polar_angularaxis_direction="clockwise",
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_bar(df: pd.DataFrame) -> go.Figure:
    """Plot bar chart of relative self consumed energy."""
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["month_name"],
            y=df["energy_consumed_relative"].round(2),
            name="Self-consumed Solar Energy [%]",
        )
    )

    average_self_consumed_energy = (
        df["energy_consumed"].sum() / df["energy_produced"].sum() * 100
    )

    fig.add_trace(
        go.Scatter(
            x=[df["month_name"].iloc[0], df["month_name"].iloc[-1]],
            y=[average_self_consumed_energy] * 2,
            name="Average Self-consumed Solar Energy [%]",
            line_color="red",
            line_dash="dot",
            mode="lines",
        )
    )

    fig.update_layout(showlegend=True)
    fig.update_yaxes(range=[0, 105], ticksuffix="%")

    st.plotly_chart(fig, use_container_width=True)


def write_statistics(df: pd.DataFrame) -> None:
    """Write summary statistics to screen."""
    total_produced = round(df["energy_produced"].sum(), 1)
    total_consumed = round(df["energy_consumed"].sum(), 1)
    cost_saved = round(total_consumed * PRICE_PER_KWH, 2)

    col_one, col_two, col_three = st.columns(3)

    with col_one:
        st.metric("Total Solar Energy Produced", f"{total_produced} kWh")
    with col_two:
        st.metric("Total Solar Energy Consumed", f"{total_consumed} kWh")
    with col_three:
        st.metric("Total Cost Savings", f"{cost_saved} €")


def main() -> None:
    """Main function."""
    st.set_page_config(page_title="Balcony Solar", page_icon="☀️")

    st.title("Blacony Solar Statistics")
    st.markdown(
        'I tracked the energy production (and consumption) of my "Balkonkraftwerk" over a '
        "full year. For the energy fed into grid I do not get disbursement so I tried to "
        "self-consume as much energy as possible. Here are the results:"
    )

    df = get_data()

    st.subheader("Energy Consumed and Fed Into Grid")
    plot_radar(df)

    st.subheader("Self-consumed Energy")
    plot_bar(df)

    st.subheader("Year Statistics")
    write_statistics(df)

    st.subheader("Conclusion")
    st.markdown(
        "I was able to self-consume about 70% of the energy produced by my solar panels over "
        "the year. This number is highly dependent on the own energy consumption curve and might "
        "be optimized further, e.g. by charging electrical devices during daytime and not at night."
    )


if __name__ == "__main__":
    main()
