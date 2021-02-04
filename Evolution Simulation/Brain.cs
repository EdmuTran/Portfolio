using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Brain : MonoBehaviour
{
    public float energyUse;

    public Vector2 swimDirection;
    public float turnForce;

    public virtual void Think(Dictionary<string,float> senses)
    {

    }

    public float GetEnergyUse()
    {
        return energyUse;
    }

    public Vector2 GetSwimDirection()
    {
        return swimDirection;
    }

    public virtual void InheritFromParent(Brain parentBrain)
    {

    }
}
